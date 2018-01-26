" Usage: $ curl -fsSLo $HOME/.vimrc https://goo.gl/uTGhhv

syntax on
set number
set numberwidth=1
set tabstop=4
set shiftwidth=4
set smartindent
set expandtab
set showcmd
set incsearch
set hlsearch
set ruler
set background=dark
set softtabstop=4
set autoindent
set shiftround
filetype on
filetype plugin indent on

" highlight column 79
if exists('+colorcolumn')
    set colorcolumn=79
else
    au BufWinEnter * let w:m2=matchadd('ErrorMsg', '\%>79v.\+', -1)
endif

" remember the last cursor position
autocmd BufReadPost *
  \ if line("'\"") > 1 && line("'\"") <= line("$") |
  \   exe "normal! g`\"" |
  \ endif
