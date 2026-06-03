import sqlite3
from pathlib import Path

import pandas as pd

# --------------------------------------------------------
# PROJECT-3: SQL Insights from Dataset (Single Script)
# --------------------------------------------------------

INPUT_FILE = Path(r"C:\Users\Ayesha Asna\Downloads\Dataset for Data Analytics (2).xlsx")
OUTPUT_DIR = Path(r"D:\DECODESLAB INTERNSHIP\PROJECT-3")
DB_FILE = OUTPUT_DIR / "project3_dataset.db"
SUMMARY_FILE = OUTPUT_DIR / "project3_sql_summary.txt"


def run_query(connection, title, query, save_csv_name=None):
    """Run SQL query, print output, and optionally save to CSV."""
    print("\n" + "=" * 80)
    print(title)
    print("-" * 80)
    print("SQL Query:")
    print(query.strip())
    print("-" * 80)

    result_df = pd.read_sql_query(query, connection)
    if result_df.empty:
        print("No records returned.")
    else:
        print(result_df.to_string(index=False))
        print(f"\nRows returned: {len(result_df)}")

    if save_csv_name:
        out_csv = OUTPUT_DIR / save_csv_name
        result_df.to_csv(out_csv, index=False, encoding="utf-8")
        print(f"Saved result to: {out_csv}")

    return result_df


def main():
    try:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

        print("=" * 80)
        print("PROJECT-3 SQL ANALYSIS STARTED")
        print("=" * 80)
        print(f"Input file: {INPUT_FILE}")

        # Load Excel data
        df = pd.read_excel(INPUT_FILE)
        df.columns = [str(c).strip() for c in df.columns]
        print(f"\nDataset loaded: {df.shape[0]} rows x {df.shape[1]} columns")
        print(f"Columns: {df.columns.tolist()}")

        # Create SQLite DB and load table
        conn = sqlite3.connect(DB_FILE)
        table_name = "orders_data"
        df.to_sql(table_name, conn, if_exists="replace", index=False)
        print(f"\nData loaded into SQLite table: {table_name}")
        print(f"Database file saved at: {DB_FILE}")

        summary_lines = [
            "PROJECT-3 SQL SUMMARY",
            "-" * 40,
            f"Input file: {INPUT_FILE}",
            f"Rows: {df.shape[0]}, Columns: {df.shape[1]}",
            f"SQLite table: {table_name}",
            "",
        ]

        # 1) SELECT query (basic preview)
        q1 = f"""
        SELECT *
        FROM {table_name}
        LIMIT 10;
        """
        run_query(conn, "1) BASIC SELECT QUERY (TOP 10 ROWS)", q1, "q1_basic_select.csv")

        # 2) WHERE + ORDER BY
        q2 = f"""
        SELECT OrderID, Date, Product, Quantity, TotalPrice, OrderStatus
        FROM {table_name}
        WHERE TotalPrice > 1000
        ORDER BY TotalPrice DESC
        LIMIT 10;
        """
        q2_df = run_query(conn, "2) WHERE + ORDER BY QUERY", q2, "q2_where_orderby.csv")
        summary_lines.append(f"High value orders found (TotalPrice > 1000): {len(q2_df)} rows in top result.")

        # 3) GROUP BY + COUNT
        q3 = f"""
        SELECT Product, COUNT(*) AS OrderCount
        FROM {table_name}
        GROUP BY Product
        ORDER BY OrderCount DESC;
        """
        q3_df = run_query(conn, "3) GROUP BY WITH COUNT", q3, "q3_groupby_count.csv")
        if not q3_df.empty:
            top_product = q3_df.iloc[0]["Product"]
            top_count = int(q3_df.iloc[0]["OrderCount"])
            summary_lines.append(f"Most ordered product: {top_product} ({top_count} orders).")

        # 4) GROUP BY + SUM + AVG (basic aggregations)
        q4 = f"""
        SELECT
            PaymentMethod,
            COUNT(*) AS TotalOrders,
            SUM(TotalPrice) AS TotalRevenue,
            AVG(TotalPrice) AS AvgOrderValue
        FROM {table_name}
        GROUP BY PaymentMethod
        ORDER BY TotalRevenue DESC;
        """
        q4_df = run_query(conn, "4) GROUP BY WITH COUNT, SUM, AVG", q4, "q4_groupby_aggregations.csv")
        if not q4_df.empty:
            top_payment = q4_df.iloc[0]["PaymentMethod"]
            top_revenue = float(q4_df.iloc[0]["TotalRevenue"])
            summary_lines.append(f"Top payment method by revenue: {top_payment} (Revenue={top_revenue:.2f}).")

        # 5) WHERE + GROUP BY + AVG (filtered insight)
        q5 = f"""
        SELECT
            OrderStatus,
            COUNT(*) AS Orders,
            AVG(TotalPrice) AS AvgOrderValue
        FROM {table_name}
        WHERE TotalPrice >= 500
        GROUP BY OrderStatus
        ORDER BY AvgOrderValue DESC;
        """
        q5_df = run_query(conn, "5) FILTERED GROUP INSIGHT (WHERE + GROUP BY + AVG)", q5, "q5_filtered_group_avg.csv")
        summary_lines.append(f"Filtered status groups (TotalPrice >= 500): {len(q5_df)} groups.")

        # Save summary report
        summary_lines.append("")
        summary_lines.append("All query outputs were printed during execution and saved as CSV files.")
        SUMMARY_FILE.write_text("\n".join(summary_lines), encoding="utf-8")

        print("\n" + "=" * 80)
        print("SUMMARY OBSERVATIONS")
        print("=" * 80)
        for line in summary_lines[5:]:
            print(line)

        print("\nSaved summary report:", SUMMARY_FILE)
        print("Saved query result files in:", OUTPUT_DIR)
        print("\n" + "=" * 80)
        print("PROJECT-3 SQL ANALYSIS COMPLETED")
        print("=" * 80)

        conn.close()

    except FileNotFoundError:
        print(f"ERROR: Input file not found -> {INPUT_FILE}")
    except PermissionError:
        print("ERROR: Permission denied while reading/saving files.")
    except Exception as error:
        print(f"ERROR: Unexpected issue occurred -> {error}")


if __name__ == "__main__":
    main()

