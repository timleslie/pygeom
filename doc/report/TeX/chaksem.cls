%%% This is a LaTeX2e document class.
%%%
%%% Customization of the `seminar' style for overhead presentations
%%%
%%% Manuel M. T. Chakravarty <chak@cse.unsw.edu.au> [1997..2000]
%%%
%%% This file is free software; you can redistribute it and/or modify
%%% it under the terms of the GNU General Public License as published by
%%% the Free Software Foundation; either version 2 of the License, or
%%% (at your option) any later version.
%%%
%%% This file is distributed in the hope that it will be useful,
%%% but WITHOUT ANY WARRANTY; without even the implied warranty of
%%% MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
%%% GNU General Public License for more details.
%%%
%%% DOCU ======================================================================
%%%
%%% * `online' option for PostScript that can be used online (otherwise, it is 
%%%   for printed slides)
%%%
%%% * `paper' for generating a four-up paper version of slides (overlays are 
%%%   collapsed onto a single page)
%%%
%%% * `helvetica' option for alternative font (is heavier, and thus, usually
%%%   better for SVGA LCD projectors)
%%%
%%% * All macros that are meant to be used by user documents (ie, the exported
%%%   macros) are having a comment starting with a template of the macro usage.
%%%
%%% Thanks to Aart Middeldorp <ami@is.tsukuba.ac.jp> for improvements.
%%%
%%% TODO ======================================================================
%%%
%%% * \slitemize is a kludge
%%%
%%% * Aart asked for better support for slide* (at least remove the bars or
%%%   provide an extra command to remove them)
%%%

\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{chaksem}[2000/11/22 v1.5a Chak's Seminar Style]

% Pipe options through to the `seminar' style
%
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{seminar}}
\DeclareOption{online}{%  overlays should accumulate
  \special{!tx@Dict begin /BeginOL { dup (all) eq exch TheOL le or { IfVisible
        not { CP OLUnit T moveto /IfVisible true def } if } { IfVisible { CP
          OLUnit NET moveto /IfVisible false def } if } ifelse } def end}%
  }
\DeclareOption{paper}{%
  \AtEndOfClass{\overlaysfalse\articlemag{1}\twoup}
  \PassOptionsToClass{article}{seminar}
  }
\DeclareOption{avantgarde}{% std font (sans serif)
  \renewcommand{\familydefault}{pag}
  }
\DeclareOption{helvetica}{% alternative heavier font (sans serif)
  \renewcommand{\familydefault}{phv}
  }
\ExecuteOptions{avantgarde}
\ProcessOptions

% seminar style including support for overlays
%
\LoadClass[semlayer,semcolor]{seminar}

% Assume a printer driver that is capable to process the landscape special
%
\renewcommand{\printlandscape}{\special{landscape}}

\RequirePackage{newcent}        % as basic font
\RequirePackage{palatino}
\RequirePackage{pifont}         % for labels in lists
\RequirePackage{ifthen}

% colours / grey scales
%
\newgray{darkgray}{.55}

% New page style, where the current heading is set in the lower left of all
% slides belonging to the heading
%
% * the lower right corner by default contains the page number, but can be
%   replaced by something else (eg, author of the talk) by re-defining
%   \thatheading
%
\newpagestyle{withheading}%
  {\thismark}{{\sc\thisheading}\hfill{\sc\thatheading}}
\def\thisheading{}
\def\thatheading{\thepage}
\pagestyle{withheading}

% Set footers
%
\newcommand{\setfooter}[1]{\setleftfooter{#1}}
\newcommand{\setleftfooter}[1]{%
  \gdef\thisheading{#1}}
\newcommand{\setrightfooter}[1]{%
  \gdef\thatheading{#1}}

% \heading[optional text for second line]{Heading text}
%
% Display a heading, which optionally may contain a second line (we can't use
% \\ in a heading text, because the same text is also displayed in the footer)
%
\newcommand{\heading}[2][!*NEVER USED ARGUMENT*!]{%
  \ifthenelse{\equal{#1}{!*NEVER USED ARGUMENT*!}}{%
    \centerline{\textbf{\textsc{\darkgray\large#2}}}%
    \vspace*{.2em}
    \par\ignorespaces%
    \setfooter{#2}
    }{%
    \begin{center}\textbf{\textsc{\darkgray\large#1\\#2}}\end{center}%
    \setfooter{#1\ldots}
    }%
  }

% OBSOLETE (since v1.2d) -- will go away
%
\newcommand{\headingx}[2]{%
  \begin{center}\textbf{\textsc{\darkgray\large#1\\#2}}\end{center}%
  \setfooter{#1 #2}}

% \subheading{heading text}
% \subheadingx{heading text}
%
% For second level headings (set in small caps and left aligned, followed by a
% colon)
%
\newcommand{\subheading}[1]{%
  \textbf{\textsc{\darkgray#1:}}}
%
% and the same without colon
%
\newcommand{\subheadingx}[1]{%
  \textbf{\textsc{\darkgray#1}}}

% \markslide
%
% Mark optional slides with \markslide (they get a star set in the lower right
% corner)
%
\def\thismark{}                 % here we store the marker
\newcommand{\markslide}{%       % mark a slide
  \def\thismark{*}}             % note: this defines \thismark *locally*

% New slide frame, consisting of two horizontal lines -- above and below the
% main material (this is less heavy than full frames, but still more
% interesting than no frame at all)
%
\let\toprulecol=\black
\let\botrulecol=\black
\newslideframe{bars}{%
  \vbox{%
%    \centerline{\toprulecol\raise1em\hbox{\rule{\textwidth}{.5pt}}}%
    \centerline{\raise1em\hbox{%
        {\toprulecol\rule{.05\textwidth}{.5pt}}%
        \rule{.9\textwidth}{.5pt}%
        {\toprulecol\rule{.05\textwidth}{.5pt}}%
        }}%
    #1%
%    \centerline{\botrulecol\rule{\textwidth}{.5pt}}%
    \centerline{%
      {\botrulecol\rule{.05\textwidth}{.5pt}}%
      \rule{.9\textwidth}{.5pt}%
      {\botrulecol\rule{.05\textwidth}{.5pt}}%
      }%
    }%
  } 
\slideframe{bars}

% \begin{slitemize}
% \item First thing
% \item Second thing
% ...
% \item Nth thing
% \end{slitemize}
%
% an itemize environment using Zapf's rounded right arrow; the items are set in
% a slightly smaller font with modified spacing
%
\newenvironment{slitemize}{%
    \begin{dinglist}{220}%
      \small
      \vspace*{-.5em}
      \setlength{\itemsep}{-.15em}
      }{
    \end{dinglist}%
    \vspace*{-.1em}%
    \ignorespaces
    }

% \begin{slumerate}
% \item First thing
% \item Second thing
% ...
% \item Nth thing
% \end{slumerate}
%
% an enumerate environment using Zapf's encircled numbers; the items are set in
% a slightly smaller font with modified spacing
%
\newenvironment{slumerate}{%
    \begin{dingautolist}{192}%
      \small
      \vspace*{-.5em}
      \setlength{\itemsep}{-.15em}
      }{
    \end{dingautolist}%
    \vspace*{-.1em}%
    \ignorespaces
    }

% for overlays
%

% \fst{stuff}
% ...
% \nin{stuff}
%
% format stuff for the second, third, and so on overlay
%
\newcommand{\fst}[1]{{\overlay{0}#1}}
\newcommand{\snd}[1]{{\overlay{1}#1}}
\newcommand{\trd}[1]{{\overlay{2}#1}}
\newcommand{\fou}[1]{{\overlay{3}#1}}
\newcommand{\fif}[1]{{\overlay{4}#1}}
\newcommand{\six}[1]{{\overlay{5}#1}}
\newcommand{\sev}[1]{{\overlay{6}#1}}
\newcommand{\eig}[1]{{\overlay{7}#1}}
\newcommand{\nin}[1]{{\overlay{8}#1}}

% \begin{first} stuff \end{first}
% ...
% \begin{ninth} stuff \end{ninth}
%
% overlays for larger chunks of text
%
\newenvironment{first}{%
  \bgroup\overlay{0}%
  }{%
  \egroup\ignorespaces
  }
\newenvironment{second}{%
  \bgroup\overlay{1}%
  }{%
  \egroup\ignorespaces
  }
\newenvironment{third}{%
  \bgroup\overlay{2}%
  }{%
  \egroup\ignorespaces
  }
\newenvironment{fourth}{%
  \bgroup\overlay{3}%
  }{%
  \egroup\ignorespaces
  }
\newenvironment{fifth}{%
  \bgroup\overlay{4}%
  }{%
  \egroup\ignorespaces
  }
\newenvironment{sixth}{%
  \bgroup\overlay{5}%
  }{%
  \egroup\ignorespaces
  }
\newenvironment{seventh}{%
  \bgroup\overlay{7}%
  }{%
  \egroup\ignorespaces
  }
\newenvironment{eight}{%
  \bgroup\overlay{8}%
  }{%
  \egroup\ignorespaces
  }
\newenvironment{ninth}{%
  \bgroup\overlay{8}%
  }{%
  \egroup\ignorespaces
  }

% \beforeafter{overlay}{stuff1}{stuff2}
%
% the third argument in a box of the same size as that used by the second
% argument, but on the overlay specified by the first argument (note that the
% second text does not *replace* the first text, but *overlays* on it)
%
% Example:
%   \beforeafter{snd}{stuff}{stuff on second overlay}
%
\makeatletter
\newcommand{\beforeafter}[3]{%
  \newif\ifouterm@th
  \ifmmode\outerm@thtrue\else\outerm@thfalse\fi
  \setbox0=\hbox{\ifouterm@th$#2$\else#2\fi}%
%  \unhcopy0\hskip-\wd0%  % doesn't work in math mode
  #2%
  \hskip-\wd0%            % this does
  \csname\string#1\expandafter\endcsname{#3}%
  }
\makeatother

% \fstsnd{stuff1}{stuff2}
% \sndtrd{stuff1}{stuff2}
%
% shorthands for frequent case of \beforeafter
%
\newcommand{\fstsnd}[2]{\fst{\beforeafter{snd}{#1}{#2}}}
\newcommand{\sndtrd}[2]{\snd{\beforeafter{trd}{#1}{#2}}}

% \eraseafter{overlay}{stuff to stroke out}
%
% stroke out in red in overlay specified in the first argument
%
\makeatletter
\newcommand{\eraseafter}[2]{%
  \newif\ifouterm@th
  \ifmmode\outerm@thtrue\else\outerm@thfalse\fi
  \setbox0=\hbox{\ifouterm@th$#2$\else#2\fi}%
%  \unhcopy0\hskip-\wd0\hskip-.15ex%
  #2\hskip-\wd0\hskip-.15ex%
  \csname\string#1\expandafter\endcsname{{%
    \red\raise.25em\hbox{\rule{\wd0}{1pt}\rule{.15ex}{1pt}}}}%
  }
\makeatother

% \snderase{stuff to stroke out}
%
% stroke out in red in second overlay
%
\newcommand{\snderase}[1]{\eraseafter{snd}{#1}}
