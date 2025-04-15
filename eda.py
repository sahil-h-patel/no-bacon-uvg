from dotenv import load_dotenv
import psycopg
import os
import sshtunnel as ssh
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def setup_conn():
    if not load_dotenv('.env'):
        print("Failed to load .env\nCheck README.md for format")
        exit()

    global db_conn
    ssh_host = os.getenv('SSH_HOST')
    ssh_user = os.getenv('SSH_USER')
    ssh_password = os.getenv('SSH_PASSWORD')
    db_name = os.getenv('DB_NAME')
    db_host = os.getenv('DB_HOST')
    db_port = int(os.getenv('DB_PORT'))
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')

    tunnel = ssh.open_tunnel(
        (ssh_host, 22),  # SSH host and port
        ssh_username=ssh_user,
        ssh_password=ssh_password,  # Or use password authentication if needed
        # Remote database bind address and port
        remote_bind_address=(db_host, db_port)
    )
    tunnel.start()
    print("Successfully established a ssh tunnel")
    db_conn = psycopg.connect(
        f"host={db_host} port={tunnel.local_bind_port} dbname={
            db_name} user={db_user} password={db_password}"
    )
    print("Successfully connected to the database!")


def plot_horror_time_series():
    with db_conn.cursor() as cur:
        query = ("""
            WITH horror as(
            SELECT genre, start_time 
            FROM user_plays u
            INNER JOIN video_game_genre g
            ON u.vid = g.vid
            INNER JOIN genre e
            ON g.gid = e.gid
            WHERE genre LIKE '%Horror%'
            ),

            all_months AS (
                SELECT generate_series(
                    DATE '2003-01-01',
                    DATE '2025-12-01',
                    interval '1 month'
                ) AS month_start
            ),

            timestamp_counts AS (
                SELECT DATE_TRUNC('month', start_time) AS month_start,COUNT(*) AS timestamp_count
                FROM horror
                GROUP BY DATE_TRUNC('month', start_time)
            )

            SELECT TO_CHAR(a.month_start, 'YYYY-MM') AS month_year,COALESCE(t.timestamp_count, 0) AS timestamp_count
            FROM all_months a
            LEFT JOIN timestamp_counts t ON a.month_start = t.month_start
            ORDER BY a.month_start
             """)
        # df = pd.read_sql(query, db_conn)
        # csv = df.to_csv('month_year_counts.csv', index=False)
        df = pd.read_csv('month_year_counts.csv')

        df['month_year'] = pd.to_datetime(df['month_year'], format='%Y-%m')

        df['year'] = df['month_year'].dt.year
        df['month'] = df['month_year'].dt.month
        # Jan, Feb, ...
        df['month_name'] = df['month_year'].dt.month_name().str[:3]

        df = df.sort_values(['year', 'month'])

        plt.figure(figsize=(4, 8))

        # Graph 3
        # sns.lineplot(
        #     data=df,
        #     x='month_year',
        #     y='timestamp_count',
        #     marker='o'
        # )
        #
        # plt.title("Timestamp Count Over Time")
        # plt.xlabel("Month-Year")
        # plt.ylabel("Count")
        # plt.xticks(rotation=45)
        # plt.tight_layout()
        # plt.show()
        # print(plt)

        # Graph 2 with months and lines representing years
        # sns.lineplot(
        #     data=df,
        #     x='month',
        #     y='timestamp_count',
        #     hue='year',
        #     marker='o'
        # )
        # print(df['year'].head(50))
        # exit()
        #
        # # Replace month numbers with month names on x-axis
        # month_labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
        #                 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        # plt.xticks(ticks=range(1, 13), labels=month_labels)
        #
        # plt.title("Monthly Timestamp Counts by Year")
        # plt.xlabel("Month")
        # plt.ylabel("Count")
        # plt.legend(title='Year')
        # plt.tight_layout()
        # plt.show()

        # Graph 3 Years with highlights
        sns.lineplot(data=df, x='month_year', y='timestamp_count',
                     marker='o', color='gray')

        highlight_df = df[df['month'].isin([9, 10])]

        # Red scatter overlay for Sept & Oct
        sns.scatterplot(data=highlight_df, x='month_year', y='timestamp_count',
                        color='red', s=80, label='Sept & Oct')

        # Set ticks to every year
        plt.gca().xaxis.set_major_locator(mdates.YearLocator())
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

        plt.title("Timestamp Counts Over Time (Highlighting Sept & Oct)")
        plt.xlabel("Year")
        plt.ylabel("Count")
        plt.xticks(rotation=90)
        plt.legend()
        plt.tight_layout()
        plt.show()
        plt.show()


setup_conn()
plot_horror_time_series()
