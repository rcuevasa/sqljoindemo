# AGENTS.md

This is an educational Python project demonstrating SQL JOIN types using SQLite.

## Essential Commands

### Setup and Run
```bash
# Create the sample database (creates joins_demo.db)
python setup_db.py

# Run all join demonstrations
python demo_joins.py
```

### Interactive Controls
- **Enter**: Next demonstration
- **v**: Toggle SQL query visibility (show/hide)  
- **q**: Quit demonstration

No build, test, or lint commands are configured for this project.

## Project Structure

```
sqlexamples/
├── README.md              # Comprehensive documentation of join types and usage
├── AGENTS.md              # This file - AI agent guidelines for project
├── demo_config.json        # Configuration file with all demonstrations (88 lines)
├── setup_db.py            # Creates SQLite database with sample data
├── demo_joins.py          # Main demonstration script (332 lines)
├── demo_joins_backup.py   # Backup of previous version
└── joins_demo.db          # SQLite database (created by setup_db.py)
```

### Database Schema

**users table:**
- `id` (INTEGER PRIMARY KEY)
- `name` (TEXT NOT NULL)
- `email` (TEXT)

**orders table:**
- `id` (INTEGER PRIMARY KEY)
- `user_id` (INTEGER, FOREIGN KEY references users.id)
- `amount` (REAL)
- `order_date` (TEXT)
- `product_id` (INTEGER, FOREIGN KEY references products.id)

**employees table:**
- `id` (INTEGER PRIMARY KEY)
- `name` (TEXT NOT NULL)
- `manager_id` (INTEGER, FOREIGN KEY references employees.id)

**products table:**
- `id` (INTEGER PRIMARY KEY)
- `name` (TEXT NOT NULL)
- `price` (REAL)

### Sample Data
- 5 users: Alice, Bob, Charlie, Diana, Eve
- 7 orders: 6 with valid user_ids, 1 orphan order (user_id=99)
- 7 employees: Hierarchical structure with managers
- 3 products: Widget A, B, C
- Users without orders: Diana, Eve

## Code Patterns and Conventions

### Database Connection Management
The code uses a context manager pattern for database connections:

```python
@contextmanager
def get_db_connection():
    """Context manager for database connections"""
    conn = sqlite3.connect('joins_demo.db')
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()
```

Usage:
```python
with get_db_connection() as conn:
    # database operations here
    # connection automatically closed
```

### JSON Configuration Pattern
Demonstrations are configured externally via `demo_config.json`:

```json
{
  "demonstrations": [
    {
      "title": "INNER JOIN DEMONSTRATION",
      "description": "...",
      "query": "SELECT ...",
      "result_title": "..."
    }
  ]
}
```

This pattern allows:
- Easy addition of new demonstrations
- No code changes required for new demos
- Clean separation of configuration and logic
- Maintainable demonstration data

### Single Demonstration Function
All demonstrations use a single generic function:

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

This eliminates code duplication and ensures consistent formatting.

### Terminal Responsiveness
The code adapts to terminal dimensions:

```python
def get_terminal_width():
    """Get terminal width, capped at 80"""
    try:
        width = shutil.get_terminal_size().columns
        return min(width, 80)
    except:
        return 80

def get_terminal_height():
    """Get terminal height"""
    try:
        return shutil.get_terminal_size().lines
    except:
        return 24
```

### Type Hints
The code uses type hints (imported from `typing`) for function parameters:
```python
def demonstrate_join(title: str, description: str, query: str, result_title: str):
```

### Function Documentation
All functions use docstrings with triple quotes. Be consistent with existing style.

### Code Organization
- Main demonstration function: `demonstrate_join()` (generic, reusable)
- Helper functions are shared (`get_db_connection()`, `print_query_result()`, `print_table()`, `wrap_text()`, `format_sql_query()`)
- Configuration loading: `load_demo_config()` (reads JSON)
- Comparison function: `demonstrate_comparison()` (shows all demos with counts)
- Functions follow snake_case convention

### Interactive Feature Pattern
Toggle functionality uses global state:

```python
# Global state for query visibility
show_query = True

def wait_for_keypress(prompt):
    global show_query
    # ... key detection logic ...
    if ch.lower() == 'v':
        show_query = not show_query
        return 'toggle'
```

## Important Gotchas

### SQLite JOIN Limitations
SQLite does NOT support `RIGHT JOIN` or `FULL OUTER JOIN` directly. These are simulated:

1. **RIGHT JOIN**: Simulated by swapping tables and using `LEFT JOIN`
2. **FULL OUTER JOIN**: Simulated using `UNION ALL` of `LEFT JOIN` results

When working with this codebase, remember that any RIGHT or FULL OUTER JOIN syntax would need to be implemented using these simulation patterns.

### Orphan Record
The sample data intentionally includes one orphan record (order with `user_id=99`) to demonstrate join behavior. Don't "fix" this - it's intentional for educational purposes.

### Database File
The `joins_demo.db` file is generated by `setup_db.py`. If database is missing or corrupted, run `setup_db.py` to regenerate it.

### Terminal Display
- Text wrapping is automatic based on terminal width
- Terminal width is capped at 80 characters for consistency
- Introduction page uses detailed view for height ≥ 20 lines
- Toggle feature requires terminal supporting raw input (most terminals do)

### Global State Management
The `show_query` global variable controls query visibility. When modifying interactive features:
- Use `global show_query` in functions that modify it
- No need for `global` declaration in functions that only read it
- Toggle persists across all demonstrations until changed again

## Code Style

- Use 4-space indentation (Python standard)
- Import standard library modules at top
- Triple-quoted docstrings for all functions
- Column aliases for clarity in joins (e.g., `u.id as user_id`)
- SQL queries formatted with consistent indentation
- Functions follow `verb_noun` naming convention (e.g., `load_demo_config`, `print_separator`)
- When adding new join demonstrations, add entry to `demo_config.json`
- JSON configuration uses consistent field names: `title`, `description`, `query`, `result_title`

## Testing

No formal tests are configured. To verify changes:
1. Run `python setup_db.py` to recreate database
2. Run `python demo_joins.py` to see the output
3. Test toggle feature by pressing 'v' during demonstrations
4. Check that all 14 demonstrations appear and produce expected results
5. Verify comparison section shows all demonstrations with correct row counts

## When Modifying This Codebase

- Preserve the educational purpose - changes should help users understand SQL joins
- Maintain clear output formatting with separators and headers
- Keep the orphan record in sample data to demonstrate edge cases
- When adding new demonstrations, follow JSON configuration pattern
- Use the single `demonstrate_join()` function for all demonstrations
- Update `demo_config.json` rather than modifying code for new demos
- Update README.md and AGENTS.md if you add new demonstrations or change behavior
- When adding new tables, update `setup_db.py` to create them and populate with sample data
- Ensure text wrapping works for long descriptions
- Test with different terminal sizes (COLUMNS=40,60,80)
- Verify toggle functionality still works after any UI changes

## Refactoring History

### Major Refactoring (March 2024)
- **Before**: 683 lines with 14 separate demonstration functions
- **After**: 332 lines Python + 88 lines JSON configuration
- **Improvements**: 38% code reduction, single demonstration function, external configuration
- **Features Added**: Terminal responsiveness, text wrapping, query toggle via 'v' key

### Key Architectural Changes
1. Introduced `demo_config.json` for demonstration data
2. Created single generic `demonstrate_join()` function
3. Added terminal width/height detection
4. Implemented text wrapping for long descriptions
5. Added interactive toggle for SQL query visibility
6. Separated demonstrations: ANTI-JOIN (A+B), JOIN+AGGREGATION (A+B), NON-EQUI JOIN (A+B)

## Backup and Version Control

- `demo_joins_backup.py`: Original version before all refactoring
- `demo_joins_old_version.py`: Version with separate demonstration functions
- `demo_joins_refactored.py`: Intermediate refactored version (for reference)
- Always keep backups when making major changes
- Consider using version control (git) for better change tracking

## Performance Considerations

- Database connections are properly closed via context managers
- No connection pooling (not needed for this scale)
- Queries are simple and efficient for demonstration purposes
- Terminal responsiveness uses efficient string operations for text wrapping
