return {

	"nvim-treesitter/nvim-treesitter",
	build = ":TSUpdate",

	-- Treesitter, konfigurasjon
	config = function()
		local config = require("nvim-treesitter.configs")
		config.setup({
			ensure_installed = { 
				"markdown", 
				"markdown_inline", 
				"lua",
				"python",
				"bash",
				"json",
				"latex",
				"yaml",
			},
			auto_install = true,
			highlight = { enable = true },
			indent = { enable = true },
		})
	end,
}
