import random
import tkinter as tk
from tkinter import messagebox, simpledialog

class SecureBankAccount:
    """Financial account with security features"""
    def __init__(self, account_id, access_code, category):
        self.account_id = account_id
        self.access_code = access_code
        self.category = category
        self.funds = 0.0
        self.phone_credit = 0.0
        self.transaction_history = []
    
    def verify_transaction(self, amount):
        """Validate transaction amount"""
        if amount <= 0 or amount > 100000:  # Reasonable limit
            raise ValueError("Invalid transaction amount")
        return True
    
    def add_funds(self, amount):
        """Credit money to account"""
        self.verify_transaction(amount)
        self.funds += amount
        self.record_transaction(f"Deposit: +${amount:.2f}")
    
    def remove_funds(self, amount):
        """Debit money from account"""
        self.verify_transaction(amount)
        if amount > self.funds:
            raise ValueError("Not enough available funds")
        self.funds -= amount
        self.record_transaction(f"Withdrawal: -${amount:.2f}")
    
    def send_money(self, amount, recipient):
        """Transfer to another account"""
        self.remove_funds(amount)
        recipient.add_funds(amount)
        self.record_transaction(f"Transfer to {recipient.account_id}: -${amount:.2f}")
        recipient.record_transaction(f"Transfer from {self.account_id}: +${amount:.2f}")
    
    def add_phone_credit(self, amount, phone_number):
        """Purchase mobile credit"""
        if len(phone_number) < 10 or not phone_number.isdigit():
            raise ValueError("Invalid phone number format")
        self.remove_funds(amount)
        self.phone_credit += amount
        self.record_transaction(f"Mobile top-up {phone_number}: -${amount:.2f}")
    
    def record_transaction(self, details):
        """Maintain transaction log"""
        self.transaction_history.append(details)
        if len(self.transaction_history) > 50:  # Keep recent 50 transactions
            self.transaction_history.pop(0)
    
    def get_account_summary(self):
        """Generate account snapshot"""
        return (f"Account: {self.account_id}\n"
                f"Type: {self.category}\n"
                f"Balance: ${self.funds:.2f}\n"
                f"Mobile Credit: ${self.phone_credit:.2f}")

class DigitalBank:
    """Core banking operations manager"""
    def __init__(self):
        self.accounts = {}
        self.load_account_data()
    
    def generate_account_id(self):
        """Create unique account identifier"""
        while True:
            new_id = f"DB{random.randint(100000, 999999)}"
            if new_id not in self.accounts:
                return new_id
    
    def create_new_account(self, account_type):
        """Establish new banking relationship"""
        valid_types = ["Personal", "Business", "Student"]
        if account_type not in valid_types:
            raise ValueError("Unsupported account category")
        
        new_id = self.generate_account_id()
        access_code = f"{random.randint(1000, 9999)}"  # Simple 4-digit code
        new_account = SecureBankAccount(new_id, access_code, account_type)
        self.accounts[new_id] = new_account
        self.save_account_data()
        return new_id, access_code
    
    def authenticate(self, account_id, access_code):
        """Verify account credentials"""
        account = self.accounts.get(account_id)
        if account and account.access_code == access_code:
            return account
        return None
    
    def load_account_data(self):
        """Retrieve stored account information"""
        try:
            with open("bank_data.txt", "r") as file:
                for line in file:
                    if line.strip():
                        parts = line.strip().split('|')
                        if len(parts) >= 5:
                            acc = SecureBankAccount(parts[0], parts[1], parts[2])
                            acc.funds = float(parts[3])
                            acc.phone_credit = float(parts[4])
                            self.accounts[parts[0]] = acc
        except FileNotFoundError:
            pass
    
    def save_account_data(self):
        """Persist account information"""
        with open("bank_data.txt", "w") as file:
            for account in self.accounts.values():
                file.write(f"{account.account_id}|{account.access_code}|"
                          f"{account.category}|{account.funds}|"
                          f"{account.phone_credit}\n")
    
    def close_account(self, account_id):
        """Terminate banking relationship"""
        if account_id in self.accounts:
            del self.accounts[account_id]
            self.save_account_data()
            return True
        return False

class BankingInterface:
    """User-friendly banking application"""
    def __init__(self):
        self.bank = DigitalBank()
        self.current_user = None
        self.setup_interface()
    
    def setup_interface(self):
        """Initialize application window"""
        self.window = tk.Tk()
        self.window.title("Digital Banking")
        self.window.geometry("450x500")
        self.show_welcome_screen()
    
    def clear_display(self):
        """Reset the display area"""
        for widget in self.window.winfo_children():
            widget.destroy()
    
    def show_welcome_screen(self):
        """Display initial options"""
        self.clear_display()
        self.current_user = None
        
        tk.Label(self.window, text="Digital Banking", 
                font=("Arial", 18)).pack(pady=20)
        
        menu_options = [
            ("Open New Account", self.open_account),
            ("Access Account", self.access_account),
            ("Quit", self.window.quit)
        ]
        
        for text, action in menu_options:
            tk.Button(self.window, text=text, command=action, 
                     width=20).pack(pady=8)
    
    def show_account_dashboard(self):
        """Display account management screen"""
        self.clear_display()
        
        tk.Label(self.window, text="Account Overview", 
                font=("Arial", 14)).pack(pady=10)
        
        summary = self.current_user.get_account_summary()
        tk.Label(self.window, text=summary).pack(pady=10)
        
        actions = [
            ("Add Money", self.deposit_funds),
            ("Withdraw Money", self.withdraw_funds),
            ("Send Money", self.transfer_funds),
            ("Mobile Services", self.mobile_services),
            ("Close Account", self.remove_account),
            ("Sign Out", self.show_welcome_screen)
        ]
        
        for text, action in actions:
            tk.Button(self.window, text=text, command=action, 
                     width=18).pack(pady=5)
    
    def open_account(self):
        """Handle new account creation"""
        account_type = simpledialog.askstring("New Account", 
                        "Account type (Personal/Business/Student):")
        if account_type and account_type.capitalize() in ["Personal", "Business", "Student"]:
            acc_id, code = self.bank.create_new_account(account_type.capitalize())
            messagebox.showinfo("Success", 
                f"Account created!\nID: {acc_id}\nAccess Code: {code}")
        elif account_type:
            messagebox.showerror("Error", "Invalid account type selected")
    
    def access_account(self):
        """Handle account login"""
        acc_id = simpledialog.askstring("Login", "Account ID:")
        code = simpledialog.askstring("Login", "Access Code:", show="*")
        
        if acc_id and code:
            account = self.bank.authenticate(acc_id, code)
            if account:
                self.current_user = account
                self.show_account_dashboard()
            else:
                messagebox.showerror("Error", "Invalid credentials")
    
    def deposit_funds(self):
        """Handle money deposit"""
        amount = simpledialog.askfloat("Deposit", "Enter amount:")
        if amount:
            try:
                self.current_user.add_funds(amount)
                self.bank.save_account_data()
                messagebox.showinfo("Success", "Deposit completed")
                self.show_account_dashboard()
            except ValueError as e:
                messagebox.showerror("Error", str(e))
    
    def withdraw_funds(self):
        """Handle money withdrawal"""
        amount = simpledialog.askfloat("Withdraw", "Enter amount:")
        if amount:
            try:
                self.current_user.remove_funds(amount)
                self.bank.save_account_data()
                messagebox.showinfo("Success", "Withdrawal completed")
                self.show_account_dashboard()
            except ValueError as e:
                messagebox.showerror("Error", str(e))
    
    def transfer_funds(self):
        """Handle money transfer"""
        recipient_id = simpledialog.askstring("Transfer", "Recipient Account ID:")
        if not recipient_id or recipient_id not in self.bank.accounts:
            messagebox.showerror("Error", "Invalid recipient account")
            return
            
        amount = simpledialog.askfloat("Transfer", "Enter amount:")
        if amount:
            try:
                self.current_user.send_money(amount, self.bank.accounts[recipient_id])
                self.bank.save_account_data()
                messagebox.showinfo("Success", "Transfer completed")
                self.show_account_dashboard()
            except ValueError as e:
                messagebox.showerror("Error", str(e))
    
    def mobile_services(self):
        """Handle mobile credit purchase"""
        phone = simpledialog.askstring("Mobile", "Phone number:")
        amount = simpledialog.askfloat("Mobile", "Top-up amount:")
        
        if phone and amount:
            try:
                self.current_user.add_phone_credit(amount, phone)
                self.bank.save_account_data()
                messagebox.showinfo("Success", "Mobile credit added")
                self.show_account_dashboard()
            except ValueError as e:
                messagebox.showerror("Error", str(e))
    
    def remove_account(self):
        """Handle account closure"""
        if messagebox.askyesno("Confirm", "Permanently close this account?"):
            self.bank.close_account(self.current_user.account_id)
            messagebox.showinfo("Success", "Account closed")
            self.show_welcome_screen()
    
    def start(self):
        """Launch the application"""
        self.window.mainloop()

if __name__ == "__main__":
    app = BankingInterface()
    app.start()