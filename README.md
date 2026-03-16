# SQL Joins Demonstration Tool

A comprehensive tool to demonstrate various SQL JOIN types and patterns using SQLite.

## Features

- **14 Different Join Demonstrations**: Comprehensive coverage of SQL join types
- **Interactive Toggle**: Press 'v' to show/hide SQL queries
- **Terminal Responsive**: Adapts display to terminal width and height
- **Text Wrapping**: Long descriptions wrap automatically for readability
- **JSON Configuration**: Easy to add/modify demonstrations via external config
- **Formatted Output**: Clean table displays with box-drawing characters

## Setup

1. Create sample database:
```bash
python setup_db.py
```

This creates a `joins_demo.db` file with four tables:
- `users`: 5 users (Alice, Bob, Charlie, Diana, Eve)
- `orders`: 7 orders (including 1 orphan order with invalid user_id)
- `employees`: 7 employees with manager hierarchy
- `products`: 3 products (Widget A, B, C)

## Run Demonstrations

```bash
python demo_joins.py
```

### Interactive Controls

- **Enter**: Next demonstration
- **v**: Toggle SQL query visibility (show/hide)
- **q**: Quit demonstration

## Configuration

Demonstrations are configured via `demo_config.json`:

```json
{
  "demonstrations": [
    {
      "title": "INNER JOIN DEMONSTRATION",
      "description": "Inner join returns only rows where there is a match in BOTH tables...",
      "query": "SELECT ...",
      "result_title": "Users who have placed orders (INNER JOIN)"
    }
  ]
}
```

### Adding New Demonstrations

To add a new join demonstration:
1. Open `demo_config.json`
2. Add a new object to `demonstrations` array
3. Include: `title`, `description`, `query`, `result_title`
4. Demo will automatically appear in sequence

## What It Shows

### Database Structure

**Users Table:**
- Alice (has 2 orders)
- Bob (has 1 order)
- Charlie (has 3 orders)
- Diana (has no orders)
- Eve (has no orders)

**Orders Table:**
- 6 orders with valid user_ids
- 1 orphan order (user_id=99) with no matching user
- Each order linked to a product

**Employees Table:**
- Alice CEO (no manager)
- Bob VP (reports to Alice)
- Charlie Manager (reports to Bob)
- Diana Manager (reports to Bob)
- Eve Developer (reports to Charlie)
- Frank Developer (reports to Charlie)
- Grace Developer (reports to Diana)

**Products Table:**
- Widget A ($50.00)
- Widget B ($100.00)
- Widget C ($150.00)

### Basic Join Types Demonstrated

1. **INNER JOIN**: Only rows with matches in BOTH tables
   - Shows 6 rows (users with orders only)
   - Eve and Diana excluded (no orders)
   - Orphan order excluded (no matching user)

2. **LEFT JOIN**: All rows from left table, matching from right
   - Shows 8 rows (all users with their orders)
   - Eve and Diana included (order columns are NULL)
   - Orphan order excluded (not in left table)

3. **LEFT JOIN (excluding NULLs)**: LEFT JOIN with WHERE clause filtering NULL values
   - Shows 6 rows (same as INNER JOIN)
   - Demonstrates filtering NULL values from LEFT JOIN result
   - Uses `WHERE order_id IS NOT NULL` to exclude unmatched rows

4. **RIGHT JOIN**: All rows from right table, matching from left
   - Shows 7 rows (all orders with user info)
   - Orphan order included (user columns are NULL)
   - Eve and Diana excluded (not in right table)
   - Simulated using swapped LEFT JOIN (SQLite limitation)

5. **FULL OUTER JOIN**: All rows from BOTH tables
   - Shows 9 rows (all users + orphan order)
   - Eve and Diana included (order columns are NULL)
   - Orphan order included (user columns are NULL)
   - Simulated using LEFT JOIN + UNION ALL (SQLite limitation)

### Advanced Join Types Demonstrated

6. **SELF JOIN**: Join a table to itself
   - Shows employees with their managers (7 rows)
   - Uses table aliases to distinguish between two instances of same table
   - Demonstrates organizational hierarchies

7. **CROSS JOIN**: Cartesian product of two tables
   - Shows all combinations of users × products (15 rows)
   - No join condition (no ON clause)
   - Demonstrates how quickly result sets can grow

8. **ANTI-JOIN (A) - Users without orders**: Find records in one table but NOT in another
   - Shows users who have NOT placed any orders (2 rows: Diana, Eve)
   - Uses LEFT JOIN with WHERE clause checking for NULL
   - Very useful for finding inactive users

9. **ANTI-JOIN (B) - Orphan orders**: Find records in one table but NOT in another
   - Shows orders with invalid user_id (1 row: orphan order)
   - Uses LEFT JOIN with WHERE clause checking for NULL
   - Very useful for identifying orphan records and data integrity issues

10. **JOIN with AGGREGATION (A) - Order summary**: Combine joins with GROUP BY and aggregate functions
    - Shows order summary per user with COUNT, SUM, AVG, MAX, MIN (5 rows)
    - Demonstrates reporting and analytics queries
    - Useful for understanding user behavior

11. **JOIN with AGGREGATION (B) - Product statistics**: Combine joins with GROUP BY and COUNT
    - Shows products ordered with frequency (3 rows)
    - Demonstrates inventory management queries
    - Useful for sales analysis

12. **MULTIPLE JOINS**: Join three or more tables in a single query
    - Shows users, their orders, and product details (8 rows)
    - Chains multiple LEFT JOIN operations
    - Demonstrates complex relationships (users → orders → products)

13. **NON-EQUI JOIN (A) - Greater than comparison**: Join using conditions other than equality (=)
    - Shows orders where order amount exceeds product price (6 rows)
    - Uses `>` operator instead of `=` in WHERE clause
    - Common use case: Finding profitable orders

14. **NON-EQUI JOIN (B) - Range comparison with BETWEEN**: Join using conditions other than equality (=)
    - Shows orders with amounts between 100 and 250 (3 rows)
    - Uses `BETWEEN` operator instead of `=` in WHERE clause
    - Common use case: Finding orders in a certain price range

## Implementation Details

### File Structure

- `demo_joins.py`: Main demonstration script (332 lines)
- `demo_config.json`: Configuration file with all demonstrations (88 lines)
- `setup_db.py`: Database setup script
- `joins_demo.db`: SQLite database (created by setup)
- `demo_joins_backup.py`: Backup of previous version

### Helper Functions

The `demo_joins.py` file includes reusable helper functions:

- `get_db_connection()`: Context manager for DB connections
- `get_terminal_width()`: Detect terminal width (capped at 80)
- `get_terminal_height()`: Detect terminal height
- `wrap_text()`: Wrap text to fit within terminal width
- `print_table()`: Display results in SQLite .mode table format
- `format_sql_query()`: Format SQL queries with proper indentation
- `print_query_result()`: Execute query and display results with toggle support
- `demonstrate_join()`: Generic demonstration function (used for all demos)
- `load_demo_config()`: Load demonstrations from JSON configuration
- `demonstrate_comparison()`: Side-by-side comparison of all join types

### Code Architecture

The refactored codebase uses a single demonstration function:

```python
def demonstrate_join(title: str, description: str, query: str, result_title: str):
    """Generic demonstration function that shows a join operation"""
    width = get_terminal_width()
    print("="*width)
    print(title)
    print("="*width)
    print(wrap_text(description, width))
    print_query_result(query, result_title)
```

All demonstrations are loaded from `demo_config.json` and executed using this single function, eliminating code duplication and making codebase much more maintainable.

## Key Concepts

### SQLite Limitations
- SQLite does NOT support `RIGHT JOIN` or `FULL OUTER JOIN` directly
- These are simulated using `LEFT JOIN` and `UNION ALL`
- This demonstrates how to work around database limitations

### Terminal Responsiveness
- Demonstrations adapt to terminal width (max 80 characters)
- Text wrapping prevents lines from exceeding terminal width
- Introduction page formats differently based on terminal height (≥20 lines for detailed view)

### Interactive Features
- Press 'v' anytime to show/hide SQL queries
- Query formatting includes proper indentation for readability
- Toggle persists across demonstrations until changed again

### Educational Value
Each demonstration includes:
- Clear explanation of join type
- Formatted SQL query (toggle with 'v' key)
- Query output showing results in table format
- Row count for result set
- Practical use cases and examples
- Comparison with other join types at end

## Usage Examples

### Basic Usage
```bash
python demo_joins.py
# Press Enter to advance through demonstrations
# Press 'v' to toggle SQL query visibility
# Press 'q' to quit
```

### Customizing Demonstrations
```bash
# Edit demo_config.json to add new demonstrations
# Format: title, description, query, result_title
# Automatically picked up on next run
```

### Terminal Testing
```bash
# Test with different terminal sizes
COLUMNS=60 LINES=20 python demo_joins.py
COLUMNS=40 LINES=15 python demo_joins.py
```

## Troubleshooting

### Database Not Found
```bash
# Run setup to create database
python setup_db.py
```

### Import Errors
```bash
# Check Python version (3.6+ required)
python3 --version
# Check for required modules (standard library only)
```

### Terminal Display Issues
- Ensure terminal supports box-drawing characters
- Try smaller terminal width if formatting looks off
- Use standard terminal, not mobile clients

## Code Statistics

- **Original Version**: 683 lines (14 separate functions)
- **Refactored Version**: 332 lines (Python) + 88 lines (JSON) = 420 total
- **Code Reduction**: 263 lines (38% smaller)
- **Maintainability**: Much improved with single function and JSON config
