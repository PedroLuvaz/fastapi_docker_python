import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
import requests
import json

API_URL = "http://localhost:8000"
access_token = None

# --- API Functions ---

def api_login(email, password):
    global access_token
    try:
        response = requests.post(f"{API_URL}/token", data={"username": email, "password": password})
        if response.status_code == 200:
            access_token = response.json()["access_token"]
            messagebox.showinfo("Success", "Login successful!")
            show_main_view()
        else:
            messagebox.showerror("Error", f"Failed to login: {response.json().get('detail', response.text)}")
    except requests.exceptions.ConnectionError as e:
        messagebox.showerror("Connection Error", f"Could not connect to the API: {e}")

def api_create_user(name, email, password):
    try:
        user_data = {"name": name, "email": email, "password": password}
        response = requests.post(f"{API_URL}/users/", json=user_data)
        if response.status_code == 201:
            messagebox.showinfo("Success", "User created successfully!")
            show_login_view()
        else:
            messagebox.showerror("Error", f"Failed to create user: {response.json().get('detail', response.text)}")
    except requests.exceptions.ConnectionError as e:
        messagebox.showerror("Connection Error", f"Could not connect to the API: {e}")

def api_get_user(user_id):
    if not access_token: return
    headers = {"Authorization": f"Bearer {access_token}"}
    try:
        response = requests.get(f"{API_URL}/users/{user_id}", headers=headers)
        if response.status_code == 200:
            user = response.json()
            return f"ID: {user['id']}\nName: {user['name']}\nEmail: {user['email']}"
        else:
            return f"Error: {response.json().get('detail', response.text)}"
    except requests.exceptions.ConnectionError:
        return "Connection Error"

def api_list_users():
    if not access_token: return
    headers = {"Authorization": f"Bearer {access_token}"}
    try:
        response = requests.get(f"{API_URL}/users/", headers=headers)
        if response.status_code == 200:
            users = response.json()
            return "\n---\n".join([f"ID: {u['id']}, Name: {u['name']}, Email: {u['email']}" for u in users])
        else:
            return f"Error: {response.json().get('detail', response.text)}"
    except requests.exceptions.ConnectionError:
        return "Connection Error"

def api_update_user(user_id, name, email):
    if not access_token: return
    headers = {"Authorization": f"Bearer {access_token}"}
    update_data = {}
    if name: update_data['name'] = name
    if email: update_data['email'] = email
    
    if not update_data:
        messagebox.showwarning("Warning", "No data to update.")
        return

    try:
        response = requests.put(f"{API_URL}/users/{user_id}", json=update_data, headers=headers)
        if response.status_code == 200:
            messagebox.showinfo("Success", "User updated successfully!")
        else:
            messagebox.showerror("Error", f"Failed to update user: {response.json().get('detail', response.text)}")
    except requests.exceptions.ConnectionError as e:
        messagebox.showerror("Connection Error", f"Could not connect to the API: {e}")

def api_delete_user(user_id):
    if not access_token: return
    headers = {"Authorization": f"Bearer {access_token}"}
    try:
        response = requests.delete(f"{API_URL}/users/{user_id}", headers=headers)
        if response.status_code == 204:
            messagebox.showinfo("Success", "User deleted successfully!")
        else:
            messagebox.showerror("Error", f"Failed to delete user: {response.json().get('detail', response.text)}")
    except requests.exceptions.ConnectionError as e:
        messagebox.showerror("Connection Error", f"Could not connect to the API: {e}")

# --- UI Handler Functions ---

def handle_login():
    api_login(login_email_entry.get(), login_password_entry.get())

def handle_create_user():
    api_create_user(create_name_entry.get(), create_email_entry.get(), create_password_entry.get())

def handle_get_user():
    user_id = get_user_id_entry.get()
    if user_id:
        result = api_get_user(user_id)
        get_user_result_label.config(text=result)

def handle_list_users():
    result = api_list_users()
    list_users_text.delete('1.0', tk.END)
    list_users_text.insert('1.0', result)

def handle_update_user():
    user_id = update_user_id_entry.get()
    name = update_name_entry.get()
    email = update_email_entry.get()
    if user_id:
        api_update_user(user_id, name, email)

def handle_delete_user():
    user_id = delete_user_id_entry.get()
    if user_id and messagebox.askyesno("Confirm", f"Are you sure you want to delete user {user_id}?"):
        api_delete_user(user_id)

# --- View Switching ---

def clear_window():
    for widget in root.winfo_children():
        widget.destroy()

def show_login_view():
    clear_window()
    root.title("Login")
    
    frame = tk.Frame(root, padx=10, pady=10)
    frame.pack()

    tk.Label(frame, text="Email").pack()
    global login_email_entry
    login_email_entry = tk.Entry(frame, width=30)
    login_email_entry.pack()

    tk.Label(frame, text="Password").pack()
    global login_password_entry
    login_password_entry = tk.Entry(frame, show="*", width=30)
    login_password_entry.pack()

    tk.Button(frame, text="Login", command=handle_login).pack(pady=10)
    tk.Button(frame, text="Create New User", command=show_create_user_view).pack()

def show_create_user_view():
    clear_window()
    root.title("Create User")

    frame = tk.Frame(root, padx=10, pady=10)
    frame.pack()

    tk.Label(frame, text="Name").pack()
    global create_name_entry
    create_name_entry = tk.Entry(frame, width=30)
    create_name_entry.pack()

    tk.Label(frame, text="Email").pack()
    global create_email_entry
    create_email_entry = tk.Entry(frame, width=30)
    create_email_entry.pack()

    tk.Label(frame, text="Password").pack()
    global create_password_entry
    create_password_entry = tk.Entry(frame, show="*", width=30)
    create_password_entry.pack()

    tk.Button(frame, text="Create User", command=handle_create_user).pack(pady=10)
    tk.Button(frame, text="Back to Login", command=show_login_view).pack()

def show_main_view():
    clear_window()
    root.title("API Client")

    notebook = ttk.Notebook(root)
    notebook.pack(pady=10, padx=10, expand=True, fill="both")

    # --- Get User Tab ---
    get_user_frame = ttk.Frame(notebook, padding="10")
    notebook.add(get_user_frame, text='Get User')
    tk.Label(get_user_frame, text="User ID:").pack()
    global get_user_id_entry
    get_user_id_entry = tk.Entry(get_user_frame, width=10)
    get_user_id_entry.pack()
    tk.Button(get_user_frame, text="Get User", command=handle_get_user).pack(pady=5)
    global get_user_result_label
    get_user_result_label = tk.Label(get_user_frame, text="", justify=tk.LEFT)
    get_user_result_label.pack(pady=10)

    # --- List Users Tab ---
    list_users_frame = ttk.Frame(notebook, padding="10")
    notebook.add(list_users_frame, text='List Users')
    tk.Button(list_users_frame, text="List All Users", command=handle_list_users).pack(pady=5)
    global list_users_text
    list_users_text = tk.Text(list_users_frame, width=60, height=15)
    list_users_text.pack()

    # --- Update User Tab ---
    update_user_frame = ttk.Frame(notebook, padding="10")
    notebook.add(update_user_frame, text='Update User')
    tk.Label(update_user_frame, text="User ID to Update:").pack()
    global update_user_id_entry
    update_user_id_entry = tk.Entry(update_user_frame, width=10)
    update_user_id_entry.pack()
    tk.Label(update_user_frame, text="New Name (optional):").pack()
    global update_name_entry
    update_name_entry = tk.Entry(update_user_frame, width=30)
    update_name_entry.pack()
    tk.Label(update_user_frame, text="New Email (optional):").pack()
    global update_email_entry
    update_email_entry = tk.Entry(update_user_frame, width=30)
    update_email_entry.pack()
    tk.Button(update_user_frame, text="Update User", command=handle_update_user).pack(pady=10)

    # --- Delete User Tab ---
    delete_user_frame = ttk.Frame(notebook, padding="10")
    notebook.add(delete_user_frame, text='Delete User')
    tk.Label(delete_user_frame, text="User ID to Delete:").pack()
    global delete_user_id_entry
    delete_user_id_entry = tk.Entry(delete_user_frame, width=10)
    delete_user_id_entry.pack()
    tk.Button(delete_user_frame, text="Delete User", command=handle_delete_user).pack(pady=10)

    # --- Logout Button ---
    tk.Button(root, text="Logout", command=show_login_view).pack(pady=10)

# --- Initial Setup ---
root = tk.Tk()
show_login_view()
root.mainloop()