-- System bruker lazy packet manager:
local lazypath = vim.fn.stdpath("data") .. "/lazy/lazy.nvim"
if not vim.loop.fs_stat(lazypath) then
	vim.fn.system({
		"git",
		"clone",
		"--filter=blob:none",
		"--branch=stable",
		"https://github.com/folke/lazy.nvim.git",
		lazypath,
	})
end
vim.opt.rtp:prepend(lazypath)

-- vim.api.nvim_create_autocmd("VimEnter", {
--	callback = function()
--		vim.cmd("cd ~/ws")
--	end,
-- })

vim.g.python3_host_prog = '/home/andreas/.neovim-venv/bin/python3'

vim.o.number = true

-- Lokal Vim-config
require("globalkeys")

-- Setup lazy.nvim with the plugins
require("lazy").setup("plugins")

-- Clipboard provider
vim.opt.clipboard = "unnamedplus"
