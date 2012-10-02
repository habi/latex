clc;clear all;close all;

[ filename, pathname] = ...
     uigetfile({'*.jpg;*.tif;*.png;*.gif','All Image Files';...
          '*.*','All Files' },'Choose Input Image');

image=imread([pathname filesep filename]);

InputDialog={'Length of the Scale Bar to draw [cm]'};
Name='Input the Details';
NumLines=1;
Defaults={'21'};
UserInput=inputdlg(InputDialog,Name,NumLines,Defaults);
scale = str2num(UserInput{1});
scale = scale * 10;  % to convert from cm to mm
figure
    imshow(image)
    hold on
    
h = helpdlg('choose start-point of scalebar','ScaleBar');
uiwait(h);
[ x1,y1 ] = ginput(1);
h = helpdlg('choose end-point of scalebar','ScaleBar');
uiwait(h);
[ x2,y2 ] = ginput(1);
    
    line([x1,x2],[y1,y2]);

length = sqrt((x1-x2)^2+(y1-y2)^2);
dpixel = scale / length * 100;
um = 100 / dpixel * 50;

    title([ 'Vectorlength: ' num2str(round(length)) 'px = ' num2str(scale) ...
        'mm, 100px = ' num2str(round(dpixel)) 'mm, ' num2str(round(um)) ...
        'px = 5 cm'])

h = helpdlg(['Image Width = ' num2str(size(image,2)) ' px - (x1,y1) = (' ...
    num2str(round(x1)) ',' num2str(round(y1)) ') - (x2, y2) = (' ...
    num2str(round(x2)) ',' num2str(round(y2)) ')'],'Positions');

disp('copy the stuff below to your .tex-file')
disp('%-------------')
disp('\newcommand{\imsize}{\linewidth}                % makes life easier with images')
disp('\newlength\imagewidth                           % needed for scalebars')
disp('\newlength\imagescale                           % needed for scalebars')
disp('\pgfmathsetlength{\imagewidth}{\imsize}         % desired displayed width of image')
disp(['\pgfmathsetlength{\imagescale}{\imagewidth/' num2str(size(image,2)) '} % pixel width of imagefile used below'])
disp('%-------------')
disp('\begin{tikzpicture}[x=\imagescale,y=-\imagescale]')
disp('  \def\x{100}')
disp('  \def\y{100}')
disp('  \node[anchor=north west,inner sep=0pt,outer sep=0pt] at (0,0)')
disp(['     {\includegraphics[width=\imagewidth]{' filename '}};' ])
disp(['	% ' num2str(round(length)) 'px = ' num2str(scale) 'mm > 100px = ' num2str(round(dpixel)) 'mm > ' num2str(round(um)) 'px = 50mm'])
disp(['	\draw[|-|,thick] (' num2str(round(x1)) ',' num2str(round(y1)) ...
    ') -- (' num2str(round(x2)) ',' num2str(round(y2)) ') node [sloped,midway,above] '...
    '{\SI{' num2str(scale) '}{\milli\meter}};' ])
disp(['	\draw[|-|,thick] (\x,\y) -- (\x+' num2str(round(um)) ',\y) node [midway,above] {\SI{5}{\centi\meter}};'])
disp('\end{tikzpicture}%');
disp('%-------------')
disp('copy the stuff above to your .tex-file')