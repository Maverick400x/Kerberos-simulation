import tkinter as tk
from tkinter import ttk, messagebox
from kdc import KDC
from service_server import ServiceServer
from client import client_login
import sys
import io


class KerberosApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Kerberos Authentication Simulation")
        self.root.geometry("600x500")
        self.root.resizable(False, False)

        # Backend setup
        self.kdc = KDC()
        self.fileserver = ServiceServer("fileserver", "fileserver_secret")

        self.build_ui()

    def build_ui(self):
        title = ttk.Label(
            self.root,
            text="Kerberos Authentication System",
            font=("Arial", 16, "bold")
        )
        title.pack(pady=15)

        form_frame = ttk.Frame(self.root)
        form_frame.pack(pady=10)

        # Username
        ttk.Label(form_frame, text="Username:").grid(row=0, column=0, pady=5, sticky="e")
        self.username_entry = ttk.Entry(form_frame, width=30)
        self.username_entry.grid(row=0, column=1, pady=5)

        # Password
        ttk.Label(form_frame, text="Password:").grid(row=1, column=0, pady=5, sticky="e")
        self.password_entry = ttk.Entry(form_frame, width=30, show="*")
        self.password_entry.grid(row=1, column=1, pady=5)

        # Service
        ttk.Label(form_frame, text="Service:").grid(row=2, column=0, pady=5, sticky="e")
        self.service_combo = ttk.Combobox(
            form_frame,
            values=["fileserver", "mailserver"],
            state="readonly",
            width=27
        )
        self.service_combo.grid(row=2, column=1, pady=5)
        self.service_combo.current(0)

        # Login button
        login_btn = ttk.Button(
            self.root,
            text="Authenticate",
            command=self.authenticate_user
        )
        login_btn.pack(pady=15)

        # Output console
        ttk.Label(self.root, text="Simulation Output:").pack()

        self.output_text = tk.Text(
            self.root,
            height=15,
            width=70,
            state="disabled",
            bg="#111",
            fg="#00FF00"
        )
        self.output_text.pack(pady=10)

    def authenticate_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        service_name = self.service_combo.get()

        if not username or not password:
            messagebox.showwarning("Input Error", "Please enter username and password.")
            return

        # Capture print output
        captured_output = io.StringIO()
        sys.stdout = captured_output

        try:
            service_server = ServiceServer(
                service_name,
                self.kdc.services[service_name]
            )

            client_login(
                self.kdc,
                username,
                password,
                service_name,
                service_server
            )

            messagebox.showinfo("Success", "Authentication successful!")

        except Exception as e:
            messagebox.showerror("Authentication Failed", str(e))

        finally:
            sys.stdout = sys.__stdout__
            self.display_output(captured_output.getvalue())

    def display_output(self, text):
        self.output_text.config(state="normal")
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, text)
        self.output_text.config(state="disabled")


if __name__ == "__main__":
    root = tk.Tk()
    app = KerberosApp(root)
    root.mainloop()