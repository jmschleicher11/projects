%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
% Location and Lacey
%
% Input csv data generated from vtp files using Paraview. This function
%   assigns an id to the particles based on their location and calculates
%   the Lacey Index based on the Deen et al. (2010) method. It generates
%   a mixing region assuming a 60 degree tapered region mixes the particles
%
% Inputs: 'filename', number of final timestep, width of domain (cm),
%   height of domain (cm), inlet width (cm), diameter (cm), orientation 
%   ('horiz' or 'vert').
%
% Outputs: creates a csv file with the particles sorted by their id and
%   has a location associated with it (file name has 'loc' before the
%   number), a figure of the mixing indes, a txt file of the Lacey index
%   values for all time steps, and outputs the final index value to the
%   screen.
%
% May 19, 2014
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%function Location_Lacey(filename,finaltime,width,height,inlet,diameter, ...
%    orientation)

filename='box256_2Umf_32cm';
finaltime=641;
width=256;
height=128;
inlet=32;
diameter=0.4;
orientation='horiz';
gridsize=4;

% filename must be entered as a string, finaltime represents final timestep

%cd('/wd2/data/csvData')
cd('/home/jmschl/Desktop/MixingCalculations/csvData')

tic                 % Call to time calculation

% Locations~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

% Read in initial timestep data to determine number of columns
vtpdata=csvread([filename,'.0.csv'],1,0);
dim=size(vtpdata);

% Check to see if the vtp files include the densities of the particles
if dim(2) == 8
    index_factor=0;
else
    index_factor=1;
end

% Columns read in are: Id, Diameter, (Density), U, V, W, X, Y, Z
sorted=sortrows(vtpdata,1);

% Checks whether user wants horizontal or vertical division of particles
typo=strcmp(orientation,'horiz');
typo=typo+strcmp(orientation,'vert');
assert(typo > 0, 'Incorrect entry for orientation')

division=strcmp(orientation,'horiz');
if division == 1
    % Calculates 1 or 0 for top or bottom half of particle domain
    location=floor(sorted(:,(7+index_factor))/(max(sorted(:,(7+ ...
        index_factor))+0.01)/2));
elseif division == 0
    % Breaks particles into 2 vertical domains
    divided_domain=width/2;
    divided_location=floor(sorted(:,(6+index_factor))/divided_domain)+1;
    % Assigns alternating 1s and 0s for the domains
    location=mod(divided_location,2);
end

% Headers to be used in file
if dim(2) == 8
    headers={'Ids', 'Diameter', 'Velocity:0', 'Velocity:1', ...
        'Velocity:2', 'Position:0', 'Position:1', 'Position:2', ...
        'Location'};
else
    headers={'Ids', 'Diameter', 'Density', 'Velocity:0', 'Velocity:1', ...
        'Velocity:2', 'Position:0', 'Position:1', 'Position:2', ...
        'Location'};
end
%~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

% Bed Heights~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
% Calculates the height of the bed, using the top 1% of particles

% Sorts particles by their height and picks the top 1%
heights=sortrows(vtpdata,(7+index_factor));
calc_one=length(heights)-floor(length(heights)*0.01);
one_percent=heights(calc_one:end,:);

% Gets the average height of the center of the particles
ave=mean(one_percent);
yave=ave((7+index_factor))+diameter/2       % prints out initial bed height
%~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

% Mixing~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
% Calculates mixing domain region width by calculating 60 degrees
%  from the inlet to the top of the particle bed
xregion=yave/tan(pi()/3); % [cm]
xwidth=2*xregion+inlet;     % [cm]
% assert(xwidth<width, 'Width of domain smaller than mixing region')

% Calculates number of mixing cells so they're 4 particle diameters
xboxes=ceil(xwidth/(diameter*gridsize));   % [boxes]
% Checks for even number
if (xboxes/2)==floor(xboxes/2)
    xboxes=xboxes;              % [boxes]
else
    xboxes=xboxes+1;            % [boxes]
end
yboxes=height/(diameter*gridsize);         % [boxes]

% Calculates where the mixing region starts in the domain
middle=width/2;    % [cm]
xstart=middle-((xboxes*diameter*gridsize)/2); % [cm]

% Creates list of bin edges (makes 1 more edge than number of bins)
% y starts at 0, x starts partway into the domain
xEdges = linspace(xstart,(xstart+xboxes*diameter*gridsize), xboxes+1);% [cm]
yEdges = linspace(0,(yboxes*diameter*gridsize), yboxes+1);         % [cm]

% Create blank arrays to store variance and ave particle numbers
%  Length of arrays is determined by number of time steps in run
Lacey_list=zeros(1,finaltime);

%~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Read in csv data, beginning with 1st row (after column headers)
%  Columns are as follows:
%  Ids  Diameters  (Densities) U  V  W  X  Y  Z
% Loops through all time steps to calculate location, variance and,
% average number of particles
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
for timestep = 0:finaltime,
    
    timestep
    
    vtpdata=csvread([filename,'.',num2str(timestep),'.csv'],1,0);
    
    assert(length(vtpdata(1,:))==(8+index_factor), ['Does this ' ...
        'simulation have two particle sizes?'])
    
    % Locations~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    % Sorts particle data by id, appends location, and writes a csv
    sorted=sortrows(vtpdata,1);
    newfile=cat(2,sorted,location);
    if division == 1
        csvwrite_with_headers([filename,'_horizloc.',num2str(timestep), ...
            '.csv'], newfile, headers, 0, 0);
    elseif division == 0
        csvwrite_with_headers([filename,'_vertloc.',num2str(timestep), ...
            '.csv'], newfile, headers, 0, 0);
    end
        
    %~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    % Mixing~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    % Calculates x-bin number and puts it in column 10 of xbinned
    [nx, binx] = histc(newfile(:,(6+index_factor)), xEdges); % [count, bin]
    xbinned = cat(2, newfile, binx);            % [bin]
    % Removes rows not in mixing region
    xbinned(xbinned(:,(10+index_factor))==0,:)=[];
    
    % Calculates y-bin number and puts it in column 11 of particles
    [ny, biny] = histc(xbinned(:,(7+index_factor)), yEdges); % [count, bin]
    particles = cat(2, xbinned, biny);          % [bin]
    
    % Calculates the average species value within the mixing region
    phi_m=mean(particles(:,(9+index_factor)));
    
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %  New columns of particles are:
    %   Ids(1) Diameter(2) U(3) V(4) W(5) X(6) Y(7) Z(8)
    %       Location(9) Xbin(10) Ybin(11)
    % OR
    %   Ids(1) Diameter(2) Densities(3) U(4) V(5) W(6) X(7) Y(8) Z(9)
    %       Location(10) Xbin(11) Ybin(12)
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    
    % Makes a cell representing each domain bin with all the
    %   particles and associated information in each bin.
    %   Multiplying the x bin by 10000 so as not to interfere with
    %   the y bin count
    binnumber = particles(:,(10+index_factor))*10000 + ...
        particles(:,(11+index_factor));
    binned = cat(2, particles, binnumber);
    bins = arrayfun(@(x) binned(binned(:, (12+index_factor)) == x, :), ...
        unique(binnumber), 'uniformoutput', false);
    
    
    % Set the minimum number of particles needed in a bin to be
    %   considered for mixing indices calculations (need at least 2
    % for averaging calculations to work correctly)
    minparticles = 2;
    for i = 1:length(bins)
        [part, col]=size(bins{i});
        if part < minparticles;
            bins{i} = NaN(size(bins{i}));
        end
        bins{i} = bins{i}(0==sum(isnan(bins{i}), 2),:);
    end
    bins = bins(~cellfun(@isempty, bins));
    Nbins=length(bins);     % Total number of bins with particles
    
    % Calculates the average number of particles in the bins
    sizescell = cellfun(@size, bins, 'uniformoutput', false);
    sizesarray = cell2mat(sizescell);
    ave_parts = mean(sizesarray(:,1));
    
    % Calculates the mean value of particle information
    meancell=cellfun(@mean, bins, 'uniformoutput', false);
    meanarray=cell2mat(meancell);
    
    phi_i=meanarray(:,(9+index_factor));  % List of concentration of 
    %  species 1 in each bin
    
    
    % Calculates the variance across the entire domain
    S_squared = sum((phi_i - phi_m).^2)/(Nbins-1);
    
    % Calculates variance: unmixed bed (S_0) and fully mixed bed (S_R)
    S_0 = phi_m*(1-phi_m);
    S_R = (phi_m*(1-phi_m))./ave_parts;
    
    Lacey = (S_squared - S_0)/(S_R - S_0);
    
    % Stores variance and the average number of particles for each
    %   time step
    Lacey_list(timestep+1) = Lacey;
end

toc         %  Ends timing

cd('/home/jmschl/Desktop/MixingCalculations/')

% Writes csv files of Lacey index for all timesteps
if gridsize == 4
    if division == 1
            csvwrite(['Lacey.',filename,'.horiz.csv'], Lacey_list);
    elseif division == 0
        csvwrite(['Lacey.',filename,'.vert.csv'], Lacey_list);
    end
else 
    if division == 1
        csvwrite(['Lacey.',filename,'.',num2str(gridsize),'.horiz.csv'],...
           Lacey_list);
    elseif division == 0
        csvwrite(['Lacey.',filename,'.',num2str(gridsize),'.vert.csv'],...
            Lacey_list);
    end
end

% Finishes by showing a plot of the Lacey index
x=0:length(Lacey_list)-1;     % Variable to plot along x-axis
writetime=1/0.125;
time=x./writetime;

plot(time,Lacey_list)
xlabel('Time (s)','FontSize',11)
ylabel('Mixing Index','FontSize',11')
ylim([0 1])
title('Lacey Mixing Index','FontSize',12)

% Prints final index value
Lacey_list(end)
%~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

cd('/home/jmschl/Repositories/magma')

% end
