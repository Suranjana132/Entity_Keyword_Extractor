import tkinter as tk
from tkinter import messagebox
from app import process_meeting_notes


def extract_information():
    try:
        # Get input
        text = input_box.get("1.0", tk.END).strip()

        # Input validation
        if not text:
            messagebox.showerror(
                "Input Error",
                "Please enter meeting notes."
            )
            return

        # Process meeting notes
        result = process_meeting_notes(text)

        # Clear previous output
        output_box.delete("1.0", tk.END)

        # Title
        output_box.insert(
            tk.END,
            "ENTITY & KEYWORD EXTRACTOR\n"
        )
        output_box.insert(
            tk.END,
            "=" * 60 + "\n\n"
        )

        # ---------------- ENTITIES ----------------

        output_box.insert(
            tk.END,
            "ENTITIES\n"
        )
        output_box.insert(
            tk.END,
            "-" * 60 + "\n"
        )

        for category, values in result["Entities"].items():

            if values:
                value_text = ", ".join(values)
            else:
                value_text = "None"

            output_box.insert(
                tk.END,
                f"{category}: {value_text}\n"
            )

        # ---------------- KEYWORDS ----------------

        output_box.insert(
            tk.END,
            "\nKEYWORDS\n"
        )
        output_box.insert(
            tk.END,
            "-" * 60 + "\n"
        )

        if result["Keywords"]:
            output_box.insert(
                tk.END,
                ", ".join(result["Keywords"])
            )
        else:
            output_box.insert(
                tk.END,
                "None"
            )

        # ---------------- ACTION ITEMS ----------------

        output_box.insert(
            tk.END,
            "\n\nACTION ITEMS\n"
        )
        output_box.insert(
            tk.END,
            "-" * 60 + "\n"
        )

        if result["Action Items"]:

            for i, item in enumerate(
                result["Action Items"],
                start=1
            ):

                output_box.insert(
                    tk.END,
                    f"\n{i}. Task: "
                    f"{item['Task']}\n"
                )

                output_box.insert(
                    tk.END,
                    f"   Responsible Person: "
                    f"{item['Responsible Person']}\n"
                )

                output_box.insert(
                    tk.END,
                    f"   Deadline: "
                    f"{item['Deadline']}\n"
                )

        else:

            output_box.insert(
                tk.END,
                "No action items detected.\n"
            )

        # ---------------- METADATA ----------------

        output_box.insert(
            tk.END,
            "\nMETADATA\n"
        )
        output_box.insert(
            tk.END,
            "-" * 60 + "\n"
        )

        for category, values in result["Metadata"].items():

            if values:
                value_text = ", ".join(values)
            else:
                value_text = "None"

            output_box.insert(
                tk.END,
                f"{category}: {value_text}\n"
            )

    except Exception as error:

        messagebox.showerror(
            "Processing Error",
            "Unable to process the meeting notes.\n\n"
            + str(error)
        )


# =========================================================
# GUI WINDOW
# =========================================================

root = tk.Tk()

root.title(
    "Entity & Keyword Extractor"
)

root.geometry(
    "950x700"
)


# ---------------- TITLE ----------------

title = tk.Label(
    root,
    text="Entity & Keyword Extractor",
    font=("Arial", 22, "bold")
)

title.pack(
    pady=15
)


# ---------------- SUBTITLE ----------------

subtitle = tk.Label(
    root,
    text=(
        "Extract entities, keywords, "
        "action items and meeting metadata"
    ),
    font=("Arial", 11)
)

subtitle.pack()


# ---------------- INPUT LABEL ----------------

input_label = tk.Label(
    root,
    text="Enter Meeting Notes",
    font=("Arial", 13, "bold")
)

input_label.pack(
    pady=(20, 5)
)


# ---------------- INPUT BOX ----------------

input_box = tk.Text(
    root,
    height=8,
    width=105,
    font=("Arial", 11)
)

input_box.pack(
    padx=20
)


# ---------------- SAMPLE INPUT ----------------

input_box.insert(
    tk.END,
    "Rahul will make the cybersecurity "
    "presentation by 25 September. "
    "Priya will review the final report. "
    "The meeting was held in Mumbai and "
    "the team discussed Python and NLP."
)


# ---------------- BUTTON ----------------

button = tk.Button(
    root,
    text="EXTRACT INFORMATION",
    command=extract_information,
    font=("Arial", 12, "bold"),
    padx=20,
    pady=8
)

button.pack(
    pady=15
)


# ---------------- OUTPUT LABEL ----------------

output_label = tk.Label(
    root,
    text="Structured Output",
    font=("Arial", 13, "bold")
)

output_label.pack()


# ---------------- OUTPUT BOX ----------------

output_box = tk.Text(
    root,
    height=20,
    width=105,
    font=("Consolas", 10)
)

output_box.pack(
    padx=20,
    pady=5
)


# ---------------- START GUI ----------------

root.mainloop()