return {
    -- Gruvbox Material
    {
        "sainnhe/gruvbox-material",
        lazy = false,
        priority = 1000,
        config = function()
            -- Set Gruvbox Material options (optional)
            vim.g.gruvbox_material_background = "medium" -- medium contrast
            vim.g.gruvbox_material_enable_italic = 1     -- enable italics
            vim.g.gruvbox_material_better_performance = 1 -- optimize for speed

            -- Apply the colorscheme
            vim.cmd("colorscheme gruvbox-material")
        end
    }
}
