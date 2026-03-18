import time
import os

# ANSI color codes for CLI visualization
class Colors:
    RESET = '\033[0m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    BG_GREEN = '\033[42m'
    BG_RED = '\033[41m'
    BG_YELLOW = '\033[43m'

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_grid(grid, highlight=None, path=None, found_paths=None, title=""):
    """
    Print the grid with color highlights.
    highlight = (row, col, color_code) - current cell being checked
    path = [(row,col), ...] - current path being explored
    found_paths = {word: [(row,col), ...]} - successfully found words
    """
    rows = len(grid)
    cols = len(grid[0])

    # Build set of cells for quick lookup
    path_set = set(path) if path else set()
    found_set = {}
    if found_paths:
        for word, fp in found_paths.items():
            for cell in fp:
                found_set[cell] = word

    print(f"\n{Colors.BOLD}{'='*50}{Colors.RESET}")
    if title:
        print(f"{Colors.BOLD}{Colors.CYAN}  {title}{Colors.RESET}")
    print(f"{Colors.BOLD}{'='*50}{Colors.RESET}")

    # Column header
    print("     ", end="")
    for c in range(cols):
        print(f"{Colors.DIM}{c:3}{Colors.RESET}", end="")
    print()
    print(f"     {'---'*cols}")

    for r in range(rows):
        print(f"{Colors.DIM}{r:3} |{Colors.RESET} ", end="")
        for c in range(cols):
            cell = (r, c)
            ch = grid[r][c]

            if highlight and (r, c) == (highlight[0], highlight[1]):
                color = highlight[2]
                print(f"{color}{Colors.BOLD} {ch} {Colors.RESET}", end="")
            elif cell in found_set:
                print(f"{Colors.BG_GREEN}{Colors.BOLD} {ch} {Colors.RESET}", end="")
            elif cell in path_set:
                print(f"{Colors.YELLOW}{Colors.BOLD} {ch} {Colors.RESET}", end="")
            else:
                print(f"  {ch}", end="")
        print()

    print(f"{Colors.BOLD}{'='*50}{Colors.RESET}\n")


def is_valid(grid, row, col, rows, cols):
    """Check if cell is within grid bounds."""
    return 0 <= row < rows and 0 <= col < cols


def search_word(grid, word, row, col, index, path, visited, found_paths, delay=0.3):
    """
    Recursive backtracking function to find a word starting from (row, col).
    index = current character index in the word we're trying to match.
    path = list of (row, col) cells in current exploration path.
    visited = set of cells already in current path.
    """
    rows = len(grid)
    cols = len(grid[0])

    # Base case: all characters matched!
    if index == len(word):
        print_grid(
            grid,
            path=path,
            found_paths=found_paths,
            title=f"✅ FOUND '{word}'! Path: {path}"
        )
        print(f"{Colors.GREEN}{Colors.BOLD}  ✅ Kata '{word}' DITEMUKAN!{Colors.RESET}")
        print(f"  Path: {' → '.join([f'({r},{c})' for r,c in path])}\n")
        time.sleep(delay * 2)
        return True

    # Out of bounds
    if not is_valid(grid, row, col, rows, cols):
        return False

    # Already visited in this path
    if (row, col) in visited:
        return False

    # Character doesn't match
    if grid[row][col] != word[index]:
        # Show mismatch in red
        print_grid(
            grid,
            highlight=(row, col, Colors.RED),
            path=path,
            found_paths=found_paths,
            title=f"🔍 Mencari '{word}' | Karakter ke-{index+1}: '{word[index]}' | Di ({row},{col}): '{grid[row][col]}' ❌ TIDAK COCOK"
        )
        print(f"  {Colors.RED}❌ ({row},{col}) = '{grid[row][col]}' ≠ '{word[index]}' → Backtrack{Colors.RESET}\n")
        time.sleep(delay * 0.5)
        return False

    # Character matches — add to path
    path.append((row, col))
    visited.add((row, col))

    print_grid(
        grid,
        highlight=(row, col, Colors.BG_YELLOW),
        path=path,
        found_paths=found_paths,
        title=f"🔍 Mencari '{word}' | Karakter ke-{index+1}: '{word[index]}' | Di ({row},{col}): '{grid[row][col]}' ✓ COCOK"
    )
    print(f"  {Colors.YELLOW}✓ ({row},{col}) = '{grid[row][col]}' cocok dengan '{word[index]}' → Lanjut{Colors.RESET}\n")
    time.sleep(delay)

    # Explore all 8 directions: right, left, down, up, and 4 diagonals
    directions = [
        (0, 1,  "→ Kanan"),
        (0, -1, "← Kiri"),
        (1, 0,  "↓ Bawah"),
        (-1, 0, "↑ Atas"),
        (1, 1,  "↘ Kanan-Bawah"),
        (1, -1, "↙ Kiri-Bawah"),
        (-1, 1, "↗ Kanan-Atas"),
        (-1, -1,"↖ Kiri-Atas"),
    ]

    for dr, dc, dir_name in directions:
        next_row, next_col = row + dr, col + dc
        print(f"  {Colors.CYAN}  Mencoba arah {dir_name} → ({next_row},{next_col}){Colors.RESET}")
        time.sleep(delay * 0.3)

        if search_word(grid, word, next_row, next_col, index + 1, path, visited, found_paths, delay):
            return True

    # BACKTRACK: no direction worked, remove current cell
    path.pop()
    visited.discard((row, col))

    print_grid(
        grid,
        highlight=(row, col, Colors.RED),
        path=path,
        found_paths=found_paths,
        title=f"⬅️  BACKTRACK dari ({row},{col}) untuk '{word}'"
    )
    print(f"  {Colors.RED}⬅️  Backtrack: tidak ada arah valid dari ({row},{col}){Colors.RESET}\n")
    time.sleep(delay * 0.5)
    return False


def find_word(grid, word, found_paths, delay=0.3):
    """Try to find a word in the grid starting from every cell."""
    rows = len(grid)
    cols = len(grid[0])

    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*50}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}  🔎 Mencari kata: '{word}'{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*50}{Colors.RESET}\n")
    time.sleep(delay)

    for r in range(rows):
        for c in range(cols):
            print(f"\n{Colors.CYAN}  ▶ Mencoba titik awal ({r},{c}) = '{grid[r][c]}'{Colors.RESET}")
            time.sleep(delay * 0.3)

            path = []
            visited = set()
            if search_word(grid, word, r, c, 0, path, visited, found_paths, delay):
                found_paths[word] = path[:]
                return True

    print(f"\n{Colors.RED}{Colors.BOLD}  ❌ Kata '{word}' TIDAK DITEMUKAN dalam grid.{Colors.RESET}\n")
    return False


def word_search(grid, words, delay=0.3):
    """Main function: search for all words in the grid."""
    clear_screen()
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*50}")
    print("   WORD SEARCH - ALGORITMA BACKTRACKING")
    print(f"{'='*50}{Colors.RESET}\n")

    print(f"{Colors.BOLD}Grid:{Colors.RESET}")
    print_grid(grid, title="Grid Awal")

    print(f"{Colors.BOLD}Kata yang dicari:{Colors.RESET}")
    for w in words:
        print(f"  • {w}")
    print()

    input(f"{Colors.YELLOW}Tekan ENTER untuk memulai pencarian...{Colors.RESET}")

    found_paths = {}
    results = {}

    for word in words:
        found = find_word(grid, word, found_paths, delay)
        results[word] = found

    # Final summary
    clear_screen()
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*50}")
    print("         HASIL AKHIR")
    print(f"{'='*50}{Colors.RESET}\n")

    print_grid(grid, found_paths=found_paths, title="Semua Kata Ditemukan")

    print(f"{Colors.BOLD}Ringkasan:{Colors.RESET}")
    for word, found in results.items():
        if found:
            path = found_paths[word]
            path_str = ' → '.join([f'({r},{c})' for r, c in path])
            print(f"  {Colors.GREEN}✅ '{word}' — DITEMUKAN{Colors.RESET}")
            print(f"     Path: {path_str}")
        else:
            print(f"  {Colors.RED}❌ '{word}' — TIDAK DITEMUKAN{Colors.RESET}")
    print()


# ─────────────────────────────────────────────
#  CONTOH GRID DAN KATA
# ─────────────────────────────────────────────
if __name__ == "__main__":
    # Grid 6x6
    grid = [
        ['K', 'U', 'C', 'I', 'N', 'G'],
        ['A', 'N', 'J', 'I', 'N', 'G'],
        ['M', 'B', 'U', 'R', 'U', 'N'],
        ['B', 'I', 'R', 'U', 'N', 'G'],
        ['A', 'P', 'I', 'K', 'A', 'N'],
        ['T', 'K', 'K', 'A', 'N', 'G'],
    ]

    words = ["KUCING", "ANJING", "BURUNG", "API"]

    # delay: waktu jeda antar langkah (detik). Kecilkan untuk lebih cepat.
    word_search(grid, words, delay=0.4)