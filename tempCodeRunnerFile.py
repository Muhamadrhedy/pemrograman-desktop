        self.btn_login = tk.Button(
            card_login,
            text="Masuk",
            font=("Segoe UI", 10, "bold"),
            bg="#2563eb",
            fg="white",
            activebackground="#1d4ed8",
            activeforeground="white",
            relief=tk.FLAT,
            bd=0,
            cursor="hand2",
            padx=15,
            pady=10,
            command=self._coba_login
        )

        self.btn_login.pack(
            fill=tk.X,
            pady=(5, 5)
        )