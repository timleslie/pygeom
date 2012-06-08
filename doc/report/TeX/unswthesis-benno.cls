%%% ====================================================================
%%%  @LaTeX-class-file{
%%%	filename	= "unswthesis-jerry.cls",
%%%	version		= "1.6a",
%%%	date		= "23 October 1995",
%%%	writtenby	= "John Zaitseff",
%%%	email		= "J.Zaitseff@unsw.edu.au",
%%%	keywords	= "LaTeX, thesis, unsw, unswthesis",
%%%	docstring	= "This file provides a thesis class for the
%%%			   University of New South Wales, Australia."
%%% }
%%% ====================================================================

% This file provides a thesis class for the School of Computer Science
% and Engineering, University of New South Wales.  It is meant to be
% used with LaTeX-2e, and exists because of the archaic standards
% required by universities all over the world with regards to thesis
% styles.
%
% As with all class files, this class is meant to be used as the exclusive
% LaTeX-2e class for the entire document.  It may be introduced in the
% document via:
%
%       \documentclass{unswthesis}
%
% As always, options may be placed before the {unswthesis}.  In this case,
% the following options are supported:
%
%       singlespacing   - Single-space the document (ie, do not apply the
%                         thesis requirements).
%       doublespacing   - Double-space the document (actually, space it
%                         1.21 times the baseline).
%       draft           - Prints the word "DRAFT" across the front page,
%                         as well as on each page (in the footer).
%       final           - Opposite of draft: do not print "DRAFT".
%
% All of the options for the Book class are also supported, namely,
%       10pt, 11pt, 12pt             (11pt is used by default)
%       letterpaper, legalpaper,
%       executivepaper, a4paper,
%       a5paper, b5paper             (a4paper used by default)
%       landscape                    (not used by default)
%       oneside, twoside             (oneside used by default)
%       openright, openany           (openany used by default)
%       onecolumn, twocolumn         (onecolumn used by default)
%       openbib                      (not used by default)
%       leqn, fleqn                  (not used by default)
%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{unswthesis-benno}%
    [1995/10/23 v1.6a University of NSW Thesis Class - with Benno mods]
\RequirePackage[dvips]{epsfig}
\RequirePackage{verbatim}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%   Changeable Parameters   %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Change these for customisation.  To change them in a LaTeX document,
% simply use \thesisuni{xxx} and \thesisschool{xxx}.

\gdef\@thesisuni{The University of New South Wales}
\gdef\@thesisschool{School of Mathematics and Statistics}

% Customise for foreign languages.

\def\supervisorname{Supervisor:}
\def\assessorname{Assessor:}
\def\abstractname{Abstract}



%%%%%%%%%%%%%%%%%%%%%
%   Class options   %
%%%%%%%%%%%%%%%%%%%%%

\newif\if@dspacing{}
\newif\if@thdraft{}
\newcommand\droptnm{final}

\DeclareOption{singlespacing}{\@dspacingfalse}
\DeclareOption{doublespacing}{\@dspacingtrue}
\DeclareOption{draft}{\@thdrafttrue\renewcommand\droptnm{draft}}
\DeclareOption{final}{\@thdraftfalse\renewcommand\droptnm{final}}
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{book}}
\ExecuteOptions{doublespacing,final}
\ProcessOptions
\LoadClass[a4paper,10pt,\droptnm]{book}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%   Draft / final options   %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\if@thdraft%
    \RequirePackage{draftcopy}%
\fi


\def\draftstamp{\special{! userdict 
       begin /bop-hook{
         gsave 90 80 translate
         90 rotate /Times-Roman findfont 100 scalefont setfont
         0 0 moveto 0.94 setgray (\today) show grestore
       }def end}}%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%   Double and single spacing   %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\newcommand{\ssp}{%
    \def\baselinestretch{1}%
    \large\normalsize\selectfont}
\newcommand{\dsp}{%
    \def\baselinestretch{1.05} % used to be 1.5
    \large\normalsize\selectfont}

% Define conditional:

\if@dspacing%
    \newcommand\s@dsp{\dsp}%
\else%
    \newcommand\s@dsp{\ssp}%
\fi

% Conditional Double-spacing environment

\def\spacing{%
    \begingroup%
    \s@dsp}%
\def\endspacing{%
    \par \vskip \parskip \vskip \baselineskip%
    \endgroup%
    \vskip -\parskip%
    \vskip -\baselineskip}

% Always single-space

\def\sspacing{%
    \begingroup%
    \ssp}%
\def\endsspacing{%
    \par \vskip \parskip \vskip \baselineskip%
    \endgroup%
    \vskip -\parskip%
    \vskip -\baselineskip}

% Execute the following ONLY if double-spacing was selected.

\if@dspacing
    % The following are from "book.cls":
    \renewcommand{\mainmatter}{%
	\cleardoublepage\@mainmattertrue\pagenumbering{arabic}\s@dsp}
    \renewcommand{\backmatter}{%
	\if@openright\cleardoublepage\else\clearpage\fi%
	%\@mainmatterfalse
	\renewcommand{\thechapter}{\Alph{chapter}}
	\renewcommand{\@chapapp}{Appendix}\setcounter{chapter}{0}}

    \renewenvironment{figure}[1][tbp]{\@float{figure}[#1]\ssp}{\end@float\s@dsp}
    \renewenvironment{figure*}[1][tbp]{\@dblfloat{figure}[#1]\ssp}{\end@dblfloat\s@dsp}
    \renewenvironment{table}[1][tbp]{\@float{table}[#1]\ssp}{\end@float\s@dsp}
    \renewenvironment{table*}[1][tbp]{\@dblfloat{table}[#1]\ssp}{\end@dblfloat\s@dsp}
    \newenvironment{blah}{\ssp\@verbatim}{\end{verbatim}\s@dsp}

    % The following are from "latex.ltx". BUG: This is NOT single-spaced.

    \long\def\@footnotetext#1{\insert\footins{%
	\ssp%                  % Should be single-spaced, but...
	\reset@font\footnotesize
	\interlinepenalty\interfootnotelinepenalty
	\splittopskip\footnotesep
	\splitmaxdepth \dp\strutbox \floatingpenalty \@MM
	\hsize\columnwidth \@parboxrestore
	\protected@edef\@currentlabel{%
	    \csname p@footnote\endcsname\@thefnmark
	}%
	\color@begingroup
	    \@makefntext{%
		\rule\z@\footnotesep\ignorespaces#1\@finalstrut\strutbox}
	\color@endgroup}}
\fi

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%   Miscellaneous Commands   %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


\newcommand{\thesisuni}[1]{\gdef\@thesisuni{#1}}
\newcommand{\thesisschool}[1]{\gdef\@thesisschool{#1}}
\newcommand{\thesistitle}[1]{\gdef\@thesistitle{#1}}
\newcommand{\thesisauthor}[1]{\gdef\@thesisauthor{#1}}
\newcommand{\thesisemail}[1]{\gdef\@thesisemail{#1}}
\newcommand{\thesisdegree}[1]{\gdef\@thesisdegree{#1}}
\newcommand{\thesisdate}[1]{\gdef\@thesisdate{#1}}
\newcommand{\thesissupervisor}[1]{\gdef\@thesissupervisor{#1}}
\newcommand{\thesisassessor}[1]{\gdef\@thesisassessor{#1}}

\newcommand{\@thesistitle}{\@latex@error{No \noexpand\thesistitle given}\@ehc}
\newcommand{\@thesisauthor}{\@latex@error{No \noexpand\thesisauthor given}\@ehc}
\newcommand{\@thesisdegree}{\@latex@error{No \noexpand\thesisdegree given}\@ehc}
\newcommand{\@thesisdate}{\@latex@error{No \noexpand\thesisdate given}\@ehc}
\newcommand{\@thesissupervisor}{\@latex@error{No \noexpand\thesissupervisor given}\@ehc}
\newcommand{\@thesisassessor}{\@latex@error{No \noexpand\thesisassessor given}\@ehc}

\renewcommand{\title}[1]{\@latex@warning{\noexpand\title is not used with this class}}
\renewcommand{\author}[1]{\@latex@warning{\noexpand\author is not used with this class}}
\renewcommand{\date}[1]{\@latex@warning{\noexpand\date is not used with this class}}

%%%%%%%%%%%%%%%%%%%%%%%%%%%
%   Thesis front matter   %
%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Title page

\newcommand{\declaration}%
{\titlepage
\vfil
`I hereby declare that this submission is my own work and that, to the
best of my knowledge and belief, it contains no material previously
published or written by another person nor material which to a
substantial extent has been accepted for the award of any other degree
or diploma of the university or other institute of higher learning,
except where due acknowledgement is made in the text'
\vskip 8em%
\begin{flushleft}
\@thesisauthor\\
\today
\end{flushleft}
\vfil
\endtitlepage
}

% Abstract environment (not defined by "book.cls")

\newenvironment{abstract}{%
    \null\vfil
    \begin{center}%
	{\Large \bfseries \abstractname}
	\@endparpenalty\@M
    \end{center}\spacing}%
    {\endspacing\par\vfil\null}

\newenvironment{acknowledgements}{%
    \null\vfil
    \begin{center}%
	{\Large \bfseries Acknowledgements}
	\@endparpenalty\@M
    \end{center}\spacing}%
    {\endspacing\par\vfil\null}

\newenvironment{copyrights and trademarks}{%
    \null\vfil
    \begin{center}%
	{\Large \bfseries Trademarks}
	\@endparpenalty\@M
    \end{center}\spacing}%
    {\endspacing\par\vfil\null\endtitlepage}

\renewcommand{\maketitle}%
    {\titlepage
	\begin{center}%
	    {\huge \@thesisuni \par}
	    {\huge \@thesisschool \par}
	    \vskip 3.5em%
	    {\epsfig{file=unswcrest-colour.eps,width=4.5cm}}%
	    \vskip 1.5em%
	    {\Huge \bfseries \textsf{\@thesistitle} \par}%
	    \vskip 1em%
	    {\Large \bf \textsf{\@thesisauthor} \par}%
	    {\normalsize \texttt{<\@thesisemail>} \par}%
	    \vskip 3em%
	    {\Large \bf \@thesisdegree \par}
	    \vskip 1em%
	     \vskip 1em
	    {\Large \@thesisdate \par}%
             \vskip 3em
             {\Large {\em \supervisorname} \@thesissupervisor \par}
	\end{center}\par
    \let\maketitle\relax}

% from book.cls, actually from 'the latex companion'
% I have added \addcontentsline so that index appears
% in the toc.

\renewenvironment{theindex}
{ \columnseprule \z@ \columnsep 35\p@
  \twocolumn[\@makeschapterhead{\indexname}]%
  \addcontentsline{toc}{chapter}{Index}
  \@mkboth{\uppercase{\indexname}}{\uppercase{\indexname}}%
  \thispagestyle{plain}\parindent\z@
  \parskip\z@ \@plus .3\p@\relax
  \let\item\@idxitem}
  {\onecolumn}

% set the toc to display down to subsubsections

\setcounter{tocdepth}{2}

% a verbatim environment that is single spaced, and returns to double
% space, if that is nesc.


\def\code{%
   \def\baselinestretch{0.8}%
   \large\footnotesize\selectfont
   \par
   \verbatim
}

\def\endcode{%
   \endverbatim
   \par\s@dsp
}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%   General Page Parameters   %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% The university requirements specify a 25mm border all around, except for
% the bottom (20mm). We actually increase this to make it more
% typographically correct. The page dimensions used were taken from "The
% LaTeX Companion", p. 85, with appropriate modifications.

%\setlength\oddsidemargin{15\p@}
%\setlength\evensidemargin{15\p@}
\setlength\oddsidemargin{15mm}
\setlength\evensidemargin{0mm}
\setlength\topmargin{5mm}
\setlength\headsep{20\p@}
\setlength\headheight{20\p@}


%\setlength\footskip{40\p@}
\setlength\marginparwidth{15\p@}
\setlength\marginparsep{\z@}
\setlength\textwidth{\paperwidth %
    \advance\textwidth -144\p@ %
    \advance\textwidth -\oddsidemargin %
    \advance\textwidth -\marginparwidth %
    \advance\textwidth -\marginparsep}
\setlength\textheight{\paperheight %
    \advance\textheight -140\p@ %
    \advance\textheight -\topmargin %
    \advance\textheight -\headheight %
    \advance\textheight -\headsep %
    \advance\textheight -\footskip}
