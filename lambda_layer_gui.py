import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import os
import threading

class LambdaLayerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("AWS Lambda Layer Generator")
        self.root.geometry("600x600")
        self.root.configure(bg='#1a1a1a')
        
        # Presets
        self.presets = {
            "python": {
                "3.8": "Python 3.8",
                "3.9": "Python 3.9", 
                "3.10": "Python 3.10",
                "3.11": "Python 3.11",
                "3.12": "Python 3.12",
                "3.13": "Python 3.13"
            },
            "node": {
                "18": "Node.js 18",
                "20": "Node.js 20",
                "22": "Node.js 22"
            }
        }
        
        # Variables
        self.package_name = tk.StringVar()
        self.version = tk.StringVar(value="3.13")
        self.runtime_type = tk.StringVar(value="python")
        self.status_var = tk.StringVar(value="Ready")
        self.use_module_type = tk.BooleanVar(value=False)
        
        # Bind package name to update layer name automatically
        self.package_name.trace('w', self.update_layer_name)
        # Bind runtime type to update version presets
        self.runtime_type.trace('w', self.update_version_presets)
        
        self.setup_ui()
        
    def update_layer_name(self, *args):
        # This function is called whenever package_name changes
        # Layer name will automatically be the same as package name
        pass
        
    def update_version_presets(self, *args):
        # Update version combobox when runtime changes
        runtime = self.runtime_type.get()
        if runtime in self.presets:
            versions = list(self.presets[runtime].keys())
            self.version_combo['values'] = versions
            # Set to first available version if current version not in new runtime
            if self.version.get() not in versions:
                self.version.set(versions[0])
        
        # Show/hide module checkbox based on runtime (only if module_frame exists)
        if hasattr(self, 'module_frame'):
            if runtime == "node":
                self.module_frame.pack(fill=tk.X, pady=(0, 20))
            else:
                self.module_frame.pack_forget()
        
    def setup_ui(self):
        # Configure style for dark theme
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure dark theme colors
        style.configure('Title.TLabel', font=('SF Pro Display', 20, 'bold'), foreground='#ffffff', background='#1a1a1a')
        style.configure('Subtitle.TLabel', font=('SF Pro Display', 12), foreground='#a0a0a0', background='#1a1a1a')
        style.configure('Input.TEntry', padding=10, fieldbackground='#2d2d2d', foreground='#ffffff', insertcolor='#ffffff')
        style.configure('Action.TButton', font=('SF Pro Display', 10, 'bold'), padding=15, foreground='#ffffff', background='#404040')
        style.configure('Primary.TButton', font=('SF Pro Display', 11, 'bold'), padding=15, foreground='#ffffff', background='#007AFF')
        style.configure('Status.TLabel', font=('SF Pro Display', 10), foreground='#00d4ff', background='#1a1a1a')
        style.configure('Label.TLabel', foreground='#ffffff', background='#1a1a1a')
        style.configure('TCombobox', fieldbackground='#2d2d2d', foreground='#ffffff', arrowcolor='#ffffff', selectbackground='#404040', selectforeground='#ffffff')
        style.configure('TProgressbar', background='#00d4ff', troughcolor='#2d2d2d')
        
        # Main container
        main_container = tk.Frame(self.root, bg='#1a1a1a', padx=40, pady=30)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header_frame = tk.Frame(main_container, bg='#1a1a1a')
        header_frame.pack(fill=tk.X, pady=(0, 30))
        
        title_label = ttk.Label(header_frame, text="Lambda Layer Generator", style='Title.TLabel')
        title_label.pack()
        
        subtitle_label = ttk.Label(header_frame, text="Create and publish AWS Lambda layers with ease", style='Subtitle.TLabel')
        subtitle_label.pack(pady=(5, 0))
        
        # Input section
        input_frame = tk.Frame(main_container, bg='#1a1a1a')
        input_frame.pack(fill=tk.X, pady=(0, 30))
        
        # Package Name
        package_frame = tk.Frame(input_frame, bg='#1a1a1a')
        package_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(package_frame, text="Package Name", font=('SF Pro Display', 11, 'bold'), 
                 foreground='#ffffff', background='#1a1a1a').pack(anchor=tk.W, pady=(0, 8))
        
        package_entry = ttk.Entry(package_frame, textvariable=self.package_name, 
                                 font=('SF Pro Display', 12), style='Input.TEntry')
        package_entry.pack(fill=tk.X)
        
        # Runtime and Version in same row
        config_frame = tk.Frame(input_frame, bg='#1a1a1a')
        config_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Runtime Type
        runtime_frame = tk.Frame(config_frame, bg='#1a1a1a')
        runtime_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        ttk.Label(runtime_frame, text="Runtime", font=('SF Pro Display', 11, 'bold'), 
                 foreground='#ffffff', background='#1a1a1a').pack(anchor=tk.W, pady=(0, 8))
        
        runtime_combo = ttk.Combobox(runtime_frame, textvariable=self.runtime_type, 
                                    values=["python", "node"], state="readonly", 
                                    font=('SF Pro Display', 12), style='Input.TEntry')
        runtime_combo.pack(fill=tk.X)
        
        # Version
        version_frame = tk.Frame(config_frame, bg='#1a1a1a')
        version_frame.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(10, 0))
        
        ttk.Label(version_frame, text="Version", font=('SF Pro Display', 11, 'bold'), 
                 foreground='#ffffff', background='#1a1a1a').pack(anchor=tk.W, pady=(0, 8))
        
        self.version_combo = ttk.Combobox(version_frame, textvariable=self.version, 
                                         state="readonly", font=('SF Pro Display', 12), 
                                         style='Input.TEntry')
        self.version_combo.pack(fill=tk.X)
        
        # Initialize version presets
        self.update_version_presets()
        
        # Module type checkbox (only for Node.js)
        self.module_frame = tk.Frame(input_frame, bg='#1a1a1a')
        self.module_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.module_checkbox = tk.Checkbutton(self.module_frame, 
                                             text="Use ES Modules (type: 'module')", 
                                             variable=self.use_module_type,
                                             font=('SF Pro Display', 11),
                                             bg='#1a1a1a', fg='#ffffff',
                                             selectcolor='#2d2d2d', activebackground='#1a1a1a',
                                             activeforeground='#ffffff')
        self.module_checkbox.pack(anchor=tk.W)
        
        # Action buttons
        button_frame = tk.Frame(main_container, bg='#1a1a1a')
        button_frame.pack(fill=tk.X, pady=(0, 30))
        
        # Primary action button
        self.primary_btn = ttk.Button(button_frame, text="Create & Publish Layer", 
                                     command=self.create_and_publish, style='Primary.TButton')
        self.primary_btn.pack(fill=tk.X, pady=(0, 10))
        
        # Secondary actions
        secondary_frame = tk.Frame(button_frame, bg='#1a1a1a')
        secondary_frame.pack(fill=tk.X)
        
        create_btn = ttk.Button(secondary_frame, text="Create Only", 
                               command=self.create_layer, style='Action.TButton')
        create_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        publish_btn = ttk.Button(secondary_frame, text="Publish Only", 
                                command=self.publish_layer, style='Action.TButton')
        publish_btn.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(5, 0))
        
        # Status section
        status_frame = tk.Frame(main_container, bg='#1a1a1a')
        status_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(status_frame, text="Status:", font=('SF Pro Display', 11, 'bold'), 
                 foreground='#ffffff', background='#1a1a1a').pack(side=tk.LEFT)
        
        status_label = ttk.Label(status_frame, textvariable=self.status_var, style='Status.TLabel')
        status_label.pack(side=tk.LEFT, padx=(10, 0))
        
        # Progress bar
        self.progress = ttk.Progressbar(status_frame, mode='indeterminate', length=200)
        self.progress.pack(side=tk.RIGHT)
        
        # Log area
        log_frame = tk.LabelFrame(main_container, text="Log Output", 
                                 font=('SF Pro Display', 11, 'bold'),
                                 bg='#1a1a1a', fg='#ffffff', padx=15, pady=15)
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        self.log_text = tk.Text(log_frame, height=8, font=('SF Mono', 10), 
                               bg='#2d2d2d', fg='#ffffff', relief=tk.FLAT,
                               padx=10, pady=10, insertbackground='#ffffff')
        scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Focus on package entry
        package_entry.focus()
        
    def log_message(self, message):
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
        
    def update_status(self, status):
        self.status_var.set(status)
        self.root.update_idletasks()
        
    def run_command(self, command, shell=True):
        try:
            # Get the directory where this script is located
            script_dir = os.path.dirname(os.path.abspath(__file__))
            
            result = subprocess.run(command, shell=shell, capture_output=True, text=True, cwd=script_dir)
            if result.returncode == 0:
                self.log_message(f"✓ {command}")
                if result.stdout:
                    self.log_message(result.stdout)
            else:
                self.log_message(f"✗ {command}")
                if result.stderr:
                    self.log_message(f"Error: {result.stderr}")
                return False
            return True
        except Exception as e:
            self.log_message(f"Exception: {str(e)}")
            return False
            
    def create_layer(self):
        if not self.package_name.get():
            messagebox.showerror("Error", "Please enter a package name")
            return
            
        def create():
            self.progress.start()
            self.update_status("Creating layer...")
            self.log_message("Starting layer creation...")
            
            success = True
            
            if self.runtime_type.get() == "python":
                success = self.create_python_layer()
            else:
                success = self.create_node_layer()
                
            self.progress.stop()
            if success:
                self.update_status("Layer created successfully")
                messagebox.showinfo("Success", "Layer created successfully!")
            else:
                self.update_status("Layer creation failed")
                messagebox.showerror("Error", "Layer creation failed. Check log for details.")
                
        threading.Thread(target=create, daemon=True).start()
        
    def create_python_layer(self):
        package = self.package_name.get()
        version = self.version.get()
        
        # Create directory structure
        if not self.run_command(f"mkdir -p {package}"):
            return False
            
        # Install package using python3 -m pip
        install_cmd = f"python3 -m pip install {package} -t {package}/python/lib/python{version}/site-packages/"
        if not self.run_command(install_cmd):
            # Try alternative pip command
            install_cmd_alt = f"pip3 install {package} -t {package}/python/lib/python{version}/site-packages/"
            if not self.run_command(install_cmd_alt):
                self.log_message("Error: pip not found. Please install pip or ensure Python is in PATH")
                return False
            
        # Create zip file
        if not self.run_command(f"zip -r {package}.zip {package}"):
            return False
            
        # Don't clean up for "Create Only" - let user inspect files
        # Clean up only happens in create_and_publish
        return True
        
    def create_node_layer(self):
        package = self.package_name.get()
        version = self.version.get()
        
        # Create directory structure
        if not self.run_command(f"mkdir -p {package}"):
            return False
            
        # Create package.json if module type is selected
        if self.use_module_type.get():
            package_json_content = f'''{{
  "name": "{package}-layer",
  "version": "1.0.0",
  "type": "module",
  "description": "AWS Lambda Layer for {package}"
}}'''
            
            package_json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), package, "package.json")
            try:
                with open(package_json_path, 'w') as f:
                    f.write(package_json_content)
                self.log_message(f"✓ Created package.json with type: module")
            except Exception as e:
                self.log_message(f"✗ Failed to create package.json: {str(e)}")
                return False
            
        # Install package using npm
        if not self.run_command(f"cd {package} && npm install {package}"):
            self.log_message("Error: npm not found. Please install Node.js and npm")
            return False
            
        # Create zip file
        if not self.run_command(f"zip -r {package}.zip {package}"):
            return False
            
        # Don't clean up for "Create Only" - let user inspect files
        # Clean up only happens in create_and_publish
        return True
        
    def publish_layer(self):
        package = self.package_name.get()
        if not package:
            messagebox.showerror("Error", "Please enter a package name")
            return
            
        if not os.path.exists(f"{package}.zip"):
            messagebox.showerror("Error", f"Layer file {package}.zip not found")
            return
            
        def publish():
            self.progress.start()
            self.update_status("Publishing layer...")
            self.log_message("Starting layer publication...")
            
            # Get correct runtime format
            runtime = self.runtime_type.get()
            version = self.version.get()
            
            if runtime == "python":
                runtime_format = f"python{version}"
            else:
                runtime_format = f"nodejs{version}.x"
            
            publish_cmd = f"aws lambda publish-layer-version --layer-name {package} --zip-file fileb://{package}.zip --compatible-runtimes {runtime_format} --compatible-architectures x86_64"
            
            success = self.run_command(publish_cmd)
            
            self.progress.stop()
            if success:
                self.update_status("Layer published successfully")
                messagebox.showinfo("Success", "Layer published successfully!")
            else:
                self.update_status("Layer publication failed")
                messagebox.showerror("Error", "Layer publication failed. Check log for details.")
                
        threading.Thread(target=publish, daemon=True).start()
        
    def create_and_publish(self):
        if not self.package_name.get():
            messagebox.showerror("Error", "Please enter a package name")
            return
            
        def create_and_publish():
            self.progress.start()
            self.update_status("Creating and publishing layer...")
            self.log_message("Starting layer creation and publication...")
            
            package = self.package_name.get()
            
            # Create layer
            if self.runtime_type.get() == "python":
                create_success = self.create_python_layer()
            else:
                create_success = self.create_node_layer()
                
            if not create_success:
                self.progress.stop()
                self.update_status("Layer creation failed")
                messagebox.showerror("Error", "Layer creation failed. Check log for details.")
                return
                
            # Get correct runtime format for publishing
            runtime = self.runtime_type.get()
            version = self.version.get()
            
            if runtime == "python":
                runtime_format = f"python{version}"
            else:
                runtime_format = f"nodejs{version}.x"
                
            # Publish layer
            publish_cmd = f"aws lambda publish-layer-version --layer-name {package} --zip-file fileb://{package}.zip --compatible-runtimes {runtime_format} --compatible-architectures x86_64"
            publish_success = self.run_command(publish_cmd)
            
            # Clean up
            self.run_command(f"rm -rf {package}.zip")
            
            self.progress.stop()
            if publish_success:
                self.update_status("Layer created and published successfully")
                messagebox.showinfo("Success", "Layer created and published successfully!")
            else:
                self.update_status("Layer publication failed")
                messagebox.showerror("Error", "Layer publication failed. Check log for details.")
                
        threading.Thread(target=create_and_publish, daemon=True).start()

def main():
    root = tk.Tk()
    app = LambdaLayerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 