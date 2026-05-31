"""
╔══════════════════════════════════════════════════════╗
║   HexSoftwares Internship — Task 3                   ║
║   Twitter Sentiment Analysis using NLP               ║
║   GUI Application (Tkinter + TextBlob)               ║
╚══════════════════════════════════════════════════════╝

GitHub Repo Name: HexSoftwares_Twitter_Sentiment_Analysis
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from textblob import TextBlob
import csv
import os
import threading
from datetime import datetime

# ─── Color Theme ───────────────────────────────────────
BG       = "#1e1e2e"
CARD     = "#2a2a3e"
ACCENT   = "#00d4aa"
POS      = "#00e676"   # Green  — Positive
NEG      = "#ff5252"   # Red    — Negative
NEU      = "#ffab40"   # Orange — Neutral
TEXT     = "#ffffff"
SUBTEXT  = "#aaaacc"
BTN_BG   = "#00d4aa"
BTN_FG   = "#1e1e2e"

# ─── Sample Tweets (demo data) ─────────────────────────
SAMPLE_TWEETS = [
    "I love this product! It's absolutely amazing and works perfectly!",
    "This is the worst experience I've ever had. Totally disappointed.",
    "The weather today is okay, nothing special.",
    "Python programming is fantastic! I enjoy every moment of coding.",
    "I hate traffic jams. They waste so much of my time.",
    "The movie was average, had some good parts and some bad parts.",
    "Excellent customer service! They resolved my issue instantly.",
    "Very bad quality. The product broke after one day of use.",
    "Just finished my morning coffee. Ready for the day.",
    "Absolutely thrilled with the results! Best decision ever made!",
    "Terrible! Would not recommend this to anyone.",
    "The food was decent, not great but not bad either.",
    "So happy today! Got my dream job offer! 🎉",
    "Feeling sad and lonely. Nobody cares anymore.",
    "The lecture was informative and well-structured.",
]

# ═══════════════════════════════════════════════════════
#  SENTIMENT ENGINE
# ═══════════════════════════════════════════════════════
def analyze_sentiment(text):
    """
    Uses TextBlob NLP to analyze sentiment.
    Returns: label, polarity score, subjectivity score, emoji
    """
    blob = TextBlob(text)
    polarity     = round(blob.sentiment.polarity, 3)
    subjectivity = round(blob.sentiment.subjectivity, 3)

    if polarity > 0.05:
        label = "POSITIVE"
        emoji = "😊"
        color = POS
    elif polarity < -0.05:
        label = "NEGATIVE"
        emoji = "😞"
        color = NEG
    else:
        label = "NEUTRAL"
        emoji = "😐"
        color = NEU

    return label, polarity, subjectivity, emoji, color


# ═══════════════════════════════════════════════════════
#  MAIN APP CLASS
# ═══════════════════════════════════════════════════════
class SentimentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("HexSoftwares — Twitter Sentiment Analysis")
        self.root.geometry("1050x700")
        self.root.configure(bg=BG)
        self.root.resizable(True, True)

        self.history = []   # store all analyzed tweets
        self.stats   = {"POSITIVE": 0, "NEGATIVE": 0, "NEUTRAL": 0}

        self._build_ui()

    # ─── BUILD UI ────────────────────────────────────────
    def _build_ui(self):

        # ── Header ──
        header = tk.Frame(self.root, bg=ACCENT, height=55)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header,
                 text="🐦  Twitter Sentiment Analysis  |  HexSoftwares AI Internship — Task 3",
                 font=("Segoe UI", 13, "bold"),
                 bg=ACCENT, fg=BG).pack(side="left", padx=20, pady=14)

        # ── Main layout ──
        main = tk.Frame(self.root, bg=BG)
        main.pack(fill="both", expand=True, padx=10, pady=8)

        # LEFT PANEL
        left = tk.Frame(main, bg=CARD, width=270)
        left.pack(side="left", fill="y", padx=(0, 10))
        left.pack_propagate(False)

        # ── Input Section ──
        tk.Label(left, text="✍  Enter Tweet / Text",
                 font=("Segoe UI", 11, "bold"),
                 bg=CARD, fg=ACCENT).pack(pady=(16, 6), padx=12, anchor="w")

        self.text_input = tk.Text(left, height=6, width=28,
                                  font=("Segoe UI", 10),
                                  bg="#111122", fg=TEXT,
                                  insertbackground=ACCENT,
                                  relief="flat", wrap="word",
                                  padx=8, pady=8)
        self.text_input.pack(padx=12, pady=(0, 6))

        self._btn(left, "🔍  Analyze Sentiment", self.analyze_single, BTN_BG)
        self._btn(left, "🧹  Clear", self.clear_input, "#444466")

        self._sep(left)

        # ── Sample Tweets ──
        tk.Label(left, text="📋  Sample Tweets",
                 font=("Segoe UI", 10, "bold"),
                 bg=CARD, fg=ACCENT).pack(pady=(4, 4), padx=12, anchor="w")

        self._btn(left, "▶  Load Sample Tweets", self.load_samples, "#5599ff")
        self._btn(left, "📁  Import CSV File",    self.import_csv,   "#aa77ff")

        self._sep(left)

        # ── Stats ──
        tk.Label(left, text="📊  Live Statistics",
                 font=("Segoe UI", 10, "bold"),
                 bg=CARD, fg=ACCENT).pack(pady=(4, 6), padx=12, anchor="w")

        self.pos_lbl = tk.Label(left, text="😊  Positive :  0",
                                font=("Segoe UI", 10, "bold"),
                                bg=CARD, fg=POS)
        self.pos_lbl.pack(anchor="w", padx=16)

        self.neg_lbl = tk.Label(left, text="😞  Negative :  0",
                                font=("Segoe UI", 10, "bold"),
                                bg=CARD, fg=NEG)
        self.neg_lbl.pack(anchor="w", padx=16)

        self.neu_lbl = tk.Label(left, text="😐  Neutral  :  0",
                                font=("Segoe UI", 10, "bold"),
                                bg=CARD, fg=NEU)
        self.neu_lbl.pack(anchor="w", padx=16)

        self.total_lbl = tk.Label(left, text="📝  Total   :  0",
                                  font=("Segoe UI", 10),
                                  bg=CARD, fg=SUBTEXT)
        self.total_lbl.pack(anchor="w", padx=16, pady=(4, 0))

        self._sep(left)
        self._btn(left, "💾  Export Results CSV", self.export_csv, "#00aa88")
        self._btn(left, "🗑  Clear All Results",   self.clear_all,  "#ff5252")

        # RIGHT PANEL
        right = tk.Frame(main, bg=BG)
        right.pack(side="left", fill="both", expand=True)

        # ── Single Result Card ──
        result_frame = tk.Frame(right, bg=CARD, bd=0)
        result_frame.pack(fill="x", pady=(0, 8))

        tk.Label(result_frame, text="🎯  Last Analysis Result",
                 font=("Segoe UI", 10, "bold"),
                 bg=CARD, fg=ACCENT).pack(anchor="w", padx=14, pady=(10, 4))

        self.result_emoji = tk.Label(result_frame, text="❓",
                                     font=("Segoe UI", 36),
                                     bg=CARD, fg=TEXT)
        self.result_emoji.pack(side="left", padx=(20, 10), pady=8)

        result_info = tk.Frame(result_frame, bg=CARD)
        result_info.pack(side="left", fill="x", expand=True)

        self.result_label = tk.Label(result_info, text="—",
                                     font=("Segoe UI", 20, "bold"),
                                     bg=CARD, fg=TEXT)
        self.result_label.pack(anchor="w")

        self.result_scores = tk.Label(result_info,
                                      text="Polarity: —   |   Subjectivity: —",
                                      font=("Segoe UI", 9),
                                      bg=CARD, fg=SUBTEXT)
        self.result_scores.pack(anchor="w")

        self.result_text_preview = tk.Label(result_info, text="",
                                            font=("Segoe UI", 8, "italic"),
                                            bg=CARD, fg=SUBTEXT,
                                            wraplength=600, justify="left")
        self.result_text_preview.pack(anchor="w")

        # ── History Table ──
        table_header = tk.Frame(right, bg=BG)
        table_header.pack(fill="x")
        tk.Label(table_header, text="📜  Analysis History",
                 font=("Segoe UI", 10, "bold"),
                 bg=BG, fg=ACCENT).pack(side="left", pady=(4, 4))

        # Treeview
        tree_frame = tk.Frame(right, bg=CARD)
        tree_frame.pack(fill="both", expand=True)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Custom.Treeview",
                        background="#1a1a2e",
                        foreground=TEXT,
                        fieldbackground="#1a1a2e",
                        rowheight=28,
                        font=("Segoe UI", 9))
        style.configure("Custom.Treeview.Heading",
                        background=CARD,
                        foreground=ACCENT,
                        font=("Segoe UI", 9, "bold"))
        style.map("Custom.Treeview",
                  background=[("selected", "#003355")])

        cols = ("#", "Tweet", "Sentiment", "Polarity", "Subjectivity")
        self.tree = ttk.Treeview(tree_frame, columns=cols,
                                 show="headings",
                                 style="Custom.Treeview")

        self.tree.heading("#",            text="#")
        self.tree.heading("Tweet",        text="Tweet / Text")
        self.tree.heading("Sentiment",    text="Sentiment")
        self.tree.heading("Polarity",     text="Polarity")
        self.tree.heading("Subjectivity", text="Subjectivity")

        self.tree.column("#",            width=35,  anchor="center")
        self.tree.column("Tweet",        width=440, anchor="w")
        self.tree.column("Sentiment",    width=100, anchor="center")
        self.tree.column("Polarity",     width=80,  anchor="center")
        self.tree.column("Subjectivity", width=90,  anchor="center")

        # Tag colors for rows
        self.tree.tag_configure("POSITIVE", foreground=POS)
        self.tree.tag_configure("NEGATIVE", foreground=NEG)
        self.tree.tag_configure("NEUTRAL",  foreground=NEU)

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical",
                                  command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)

        # ── Status bar ──
        self.statusbar = tk.Label(self.root,
                                  text="Ready  |  HexSoftwares Sentiment Analysis  |  Powered by TextBlob NLP",
                                  font=("Segoe UI", 8),
                                  bg="#111122", fg=SUBTEXT, anchor="w")
        self.statusbar.pack(fill="x", side="bottom", padx=10, pady=2)

    # ─── HELPER WIDGETS ──────────────────────────────────
    def _btn(self, parent, text, cmd, color=BTN_BG):
        fg = BTN_FG if color == BTN_BG else TEXT
        tk.Button(parent, text=text, command=cmd,
                  font=("Segoe UI", 9, "bold"),
                  bg=color, fg=fg, relief="flat",
                  cursor="hand2", pady=7,
                  activebackground=ACCENT,
                  activeforeground=BG).pack(fill="x", padx=12, pady=3)

    def _sep(self, parent):
        tk.Frame(parent, bg="#444466", height=1).pack(fill="x", padx=10, pady=6)

    # ─── CORE ANALYZE ────────────────────────────────────
    def _do_analyze(self, text):
        """Analyze one tweet and add to table + history."""
        text = text.strip()
        if not text:
            return

        label, polarity, subjectivity, emoji, color = analyze_sentiment(text)

        # Update result card
        self.result_emoji.config(text=emoji, fg=color)
        self.result_label.config(text=f"{emoji}  {label}", fg=color)
        self.result_scores.config(
            text=f"Polarity: {polarity}   |   Subjectivity: {subjectivity}")
        preview = text if len(text) <= 80 else text[:77] + "..."
        self.result_text_preview.config(text=f'"{preview}"')

        # Add to history
        idx = len(self.history) + 1
        self.history.append({
            "id": idx, "text": text,
            "sentiment": label,
            "polarity": polarity,
            "subjectivity": subjectivity,
            "emoji": emoji
        })

        # Add to treeview
        short = text if len(text) <= 65 else text[:62] + "..."
        self.tree.insert("", "end",
                         values=(idx, short, f"{emoji} {label}",
                                 polarity, subjectivity),
                         tags=(label,))

        # Scroll to latest
        children = self.tree.get_children()
        if children:
            self.tree.see(children[-1])

        # Update stats
        self.stats[label] += 1
        self._update_stats()
        self.statusbar.config(
            text=f"✅  Analyzed: '{short}' → {label}  |  Total: {len(self.history)}")

    def _update_stats(self):
        self.pos_lbl.config(text=f"😊  Positive :  {self.stats['POSITIVE']}")
        self.neg_lbl.config(text=f"😞  Negative :  {self.stats['NEGATIVE']}")
        self.neu_lbl.config(text=f"😐  Neutral  :  {self.stats['NEUTRAL']}")
        total = sum(self.stats.values())
        self.total_lbl.config(text=f"📝  Total    :  {total}")

    # ─── BUTTONS ─────────────────────────────────────────
    def analyze_single(self):
        text = self.text_input.get("1.0", "end").strip()
        if not text:
            messagebox.showwarning("Empty!", "Please enter some text to analyze.")
            return
        self._do_analyze(text)

    def clear_input(self):
        self.text_input.delete("1.0", "end")

    def load_samples(self):
        self.statusbar.config(text="Loading sample tweets...")
        for tweet in SAMPLE_TWEETS:
            self._do_analyze(tweet)
        self.statusbar.config(
            text=f"✅  {len(SAMPLE_TWEETS)} sample tweets analyzed!")

    def import_csv(self):
        path = filedialog.askopenfilename(
            title="Select CSV file",
            filetypes=[("CSV Files", "*.csv"), ("Text Files", "*.txt")]
        )
        if not path:
            return

        # ── Ask how many rows to process ──
        limit_win = tk.Toplevel(self.root)
        limit_win.title("Row Limit")
        limit_win.geometry("320x180")
        limit_win.configure(bg=CARD)
        limit_win.resizable(False, False)
        limit_win.grab_set()

        tk.Label(limit_win, text="⚙  How many rows to analyze?",
                 font=("Segoe UI", 11, "bold"),
                 bg=CARD, fg=ACCENT).pack(pady=(18, 6))
        tk.Label(limit_win,
                 text="(Large files can hang the app — keep it under 200)",
                 font=("Segoe UI", 8), bg=CARD, fg=SUBTEXT).pack()

        limit_var = tk.IntVar(value=100)
        frame = tk.Frame(limit_win, bg=CARD)
        frame.pack(pady=10)
        for val, label in [(50,"50"),(100,"100"),(200,"200"),(500,"500")]:
            tk.Radiobutton(frame, text=label, variable=limit_var, value=val,
                           bg=CARD, fg=TEXT, selectcolor=BG,
                           activebackground=CARD,
                           font=("Segoe UI", 10)).pack(side="left", padx=8)

        def start():
            limit = limit_var.get()
            limit_win.destroy()
            # Run in background thread so GUI doesn't freeze
            threading.Thread(
                target=self._csv_worker,
                args=(path, limit),
                daemon=True
            ).start()

        tk.Button(limit_win, text="✅  Start Analysis",
                  command=start,
                  font=("Segoe UI", 10, "bold"),
                  bg=ACCENT, fg=BG, relief="flat",
                  cursor="hand2", pady=6).pack(fill="x", padx=30)

    def _csv_worker(self, path, limit):
        """Runs in background thread — reads CSV row by row safely."""
        import time
        count = 0
        skipped = 0

        self.root.after(0, lambda: self.statusbar.config(
            text=f"⏳  Loading CSV... processing up to {limit} rows"))

        # Common text column names to try
        TEXT_COLS = ["content", "text", "tweet", "body",
                     "message", "Content", "Text", "Tweet"]

        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                reader = csv.DictReader(f)
                headers = reader.fieldnames or []

                # Auto-detect which column has tweet text
                text_col = None
                for col in TEXT_COLS:
                    if col in headers:
                        text_col = col
                        break

                # Detect language column if present
                lang_col = "language" if "language" in headers else None

                for row in reader:
                    if count >= limit:
                        break

                    # Get tweet text
                    if text_col:
                        text = row.get(text_col, "").strip()
                    else:
                        # Fallback: pick longest cell
                        text = max(row.values(), key=len, default="").strip()

                    # Skip empty, headers, or non-English
                    if not text or len(text) < 5:
                        skipped += 1
                        continue

                    # Skip non-English if language column exists
                    if lang_col:
                        lang = row.get(lang_col, "en").strip()
                        if lang and lang != "en":
                            skipped += 1
                            continue

                    # Skip URLs-only tweets
                    if text.startswith("http") and len(text.split()) <= 2:
                        skipped += 1
                        continue

                    count += 1
                    self.root.after(0, self._do_analyze, text)
                    self.root.after(0, lambda c=count, lim=limit: self.statusbar.config(
                        text=f"⏳  Processing tweet {c} of {lim}..."))

                    time.sleep(0.04)  # keeps GUI smooth

            # Done!
            self.root.after(0, lambda: messagebox.showinfo(
                "Done! ✅",
                f"CSV Analysis Complete!\n\n"
                f"✅ Analyzed : {count} tweets\n"
                f"⏭ Skipped  : {skipped} rows\n"
                f"📊 Check stats panel for summary!"
            ))
            self.root.after(0, lambda: self.statusbar.config(
                text=f"✅  Done! {count} analyzed | {skipped} skipped"))

        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror(
                "Error", f"Could not read file:\n{e}"))

    def export_csv(self):
        if not self.history:
            messagebox.showwarning("No Data", "No results to export yet!")
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv")],
            initialfile=f"sentiment_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        )
        if not path:
            return
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f,
                fieldnames=["id","text","sentiment","polarity","subjectivity"])
            writer.writeheader()
            writer.writerows(self.history)
        messagebox.showinfo("Exported!", f"Results saved to:\n{path}")
        self.statusbar.config(text=f"💾  Exported {len(self.history)} results to CSV")

    def clear_all(self):
        if not self.history:
            return
        if messagebox.askyesno("Clear All", "Delete all analysis history?"):
            self.history.clear()
            self.stats = {"POSITIVE": 0, "NEGATIVE": 0, "NEUTRAL": 0}
            for item in self.tree.get_children():
                self.tree.delete(item)
            self.result_emoji.config(text="❓", fg=TEXT)
            self.result_label.config(text="—", fg=TEXT)
            self.result_scores.config(text="Polarity: —   |   Subjectivity: —")
            self.result_text_preview.config(text="")
            self._update_stats()
            self.statusbar.config(text="🗑  All results cleared.")


# ═══════════════════════════════════════════════════════
#  ENTRY POINT
# ═══════════════════════════════════════════════════════
if __name__ == "__main__":
    root = tk.Tk()
    app = SentimentApp(root)
    root.mainloop()
