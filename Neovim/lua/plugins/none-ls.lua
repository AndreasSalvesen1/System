return {
	"nvimtools/none-ls.nvim",
	config = function()
		local null_ls = require("null-ls")
		null_ls.setup({
			sources = {
				null_ls.builtins.formatting.stylua,
				null_ls.builtins.formatting.black,
				null_ls.builtins.formatting.isort,
				--		null_ls.builtins.diagnostics.pylint.with({
				--				command = "/home/andreas/.neovim-venv/bin/pylint"}),
				--            },
				null_ls.builtins.diagnostics.pylint,
			},
		})

		-- Define global keymap for formatting
		vim.keymap.set("n", "<leader>f", function()
			vim.lsp.buf.format({
				timeout_ms = 10000, -- 10 sec timeout
			})
		end, { desc = "Format the current buffer" })
	end,



	vim.api.nvim_create_user_command("BufferDiagnosticsQuickfix", function()
		vim.diagnostic.setqflist({ open = true, scope = "buffer" })
	end, {}),

	vim.keymap.set("n", "<C-n>", function()
		vim.diagnostic.goto_next({ severity = vim.diagnostic.severity.ERROR })
	end, { desc = "Go to next error" }),

	vim.keymap.set("n", "<C-p>", function()
		vim.diagnostic.goto_prev({ severity = vim.diagnostic.severity.ERROR })
	end, { desc = "Go to previous error" })

}
