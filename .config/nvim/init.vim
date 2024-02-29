" General Config
set relativenumber

" Configuración para vim-plug
call plug#begin('~/.local/share/nvim/plugged')

" Añade los plugins aquí
Plug 'preservim/nerdtree' "Nerd Tree (Left Files Tree)
Plug 'projekt0n/github-nvim-theme' "Github Themes
Plug 'junegunn/fzf', { 'do': { -> fzf#install() } }
Plug 'tpope/vim-fugitive'
Plug 'vim-airline/vim-airline'
Plug 'Vimjas/vim-python-pep8-indent'
Plug 'vim-scripts/sh.vim'
Plug 'ryanoasis/vim-devicons'
Plug 'Townk/vim-autoclose'
Plug 'mattn/emmet-vim'
"Plug 'neoclide/coc.nvim', {'branch': 'release'}

" Termina la sección de plugins de vim-plug
call plug#end()
colorscheme github_dark_high_contrast
" Activar NERDTree automáticamente al iniciar Neovim
autocmd VimEnter * NERDTree

" Mapear atajos de teclado para abrir y cerrar NERDTree
map <C-n> :NERDTreeToggle<CR>
" Alternar entre NERDTree y ventana de edición con Ctrl + Enter
nnoremap <C-CR> :wincmd w<CR>
" Cambiar la forma del cursor a una línea vertical
set guicursor=n-v-c:block-Cursor
" Ajustar el tamaño de las tabulaciones a 4 espacios
set tabstop=4
set softtabstop=4
set shiftwidth=4
" Cierra NerdTree cuando se abre un archivo
let g:NERDTreeQuitOnOpen = 1
set guicursor=a:ver100

" Configuracion del clipboard
set clipboard+=unnamedplus
set clipboard+=unnamed
set clipboard+=unnamedplus
