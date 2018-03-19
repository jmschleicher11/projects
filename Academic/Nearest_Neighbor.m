%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
% Nearest_Neighbor (Now called Initial Neighbor Distance)
%
% Input csv data generated from vtp files using Paraview. This file 
%   calculates the Nearest Neighbor mixing index as described in Deen et
%   al. (2010). The nice thing about this is it doesn't rely on coloring 
%   the particles.
%
% Inputs: 'filename', number of final timestep, width of domain (cm),
%   height of domain (cm), inlet width (cm), diameter (cm), minimum 
%   velocity (cm/s)
%
% Outputs: creates a figure of the mixing index, and a text file of the 
%   value of the mixing index for all time steps. 
%
% May 2, 2015
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Initial inputs for run
filename='box256_interp_test';
finaltime=639;
width=256;
height=128;
inlet=32;
diameter=0.4;
min_vel=0.8;

cd('/home/jmschl/Desktop/MixingCalculations/csvData')

tic                 % Call to time calculation

% Read in second timestep data to determine which particles to use in the
%  calculation. Timesteps 0 and 1 both have velocities of 0
% Columns read in are: Id, Diameter, (Density), U, V, W, X, Y, Z
vtpdata=csvread([filename,'.4.csv'],1,0);
vtpdata=sortrows(vtpdata,1);
dim=size(vtpdata);

% Check to see if the vtp files include the densities of the particles
if dim(2) == 8
    index_factor=0;
else
    index_factor=1;
end

% UNCOMMENT IF SAVING CSV FILES
% Headers to be used in file
% if dim(2) == 8
%     headers={'Ids', 'Diameter', 'Velocity:0', 'Velocity:1', ...
%         'Velocity:2', 'Position:0', 'Position:1', 'Position:2', ...
%         'Location'};
% else
%     headers={'Ids', 'Diameter', 'Density', 'Velocity:0', 'Velocity:1', ...
%         'Velocity:2', 'Position:0', 'Position:1', 'Position:2', ...
%         'Location'};
% end


% Bed Heights~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
% Calculates the height of the bed, using the top 1% of particles

zerodata=csvread([filename,'.0.csv'],1,0);
sorted=sortrows(zerodata,1);

% Sorts particles by their height and picks the top 1%
heights=sortrows(zerodata,(7+index_factor));
calc_one=length(heights)-floor(length(heights)*0.01);
one_percent=heights(calc_one:end,:);

% Gets the average height of the center of the particles
ave=mean(one_percent);
yave=ave((7+index_factor))+diameter/2;      % prints out initial bed height
%~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

% Mixing~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
% Calculates mixing domain region width by calculating 60 degrees
%  from the inlet to the top of the particle bed
xregion=yave/tan(pi()/3); % [cm]
xmin=width/2-(xregion+inlet/2);
xmax=width/2+(xregion+inlet/2);


% Calculates the magnitude of the velocities of the particles
velocities=sqrt(vtpdata(:,3+index_factor).^2 + ...
    vtpdata(:,4+index_factor).^2);
new_data=cat(2,sorted,velocities);
mixing_particles=new_data(new_data(:,end)>min_vel,:);
mixing_particles=mixing_particles(mixing_particles(:,6+index_factor) ...
    >=xmin,:);
mixing_particles=mixing_particles(mixing_particles(:,6+index_factor) ...
    <=xmax,:);

new_data(new_data(:,end)<=min_vel,end)=0;
new_data(new_data(:,end)>0,end)=1;
new_data(new_data(:,6+index_factor)<xmin,end)=0;
new_data(new_data(:,6+index_factor)>xmax,end)=0;
index_list=cat(2,new_data(:,1),new_data(:,end));

neighbors=zeros(length(mixing_particles),1);
randoms=zeros(length(mixing_particles),1);
particle_list=zeros(length(mixing_particles),1);

% Loop to find every particle's nearest neighbor and random partner
for particle=1:length(mixing_particles)

    particle
    
    poi=mixing_particles(particle,:);     % Particle of interest (poi) data
    loc=mixing_particles;                 % New list to keep sorted
    loc(particle,:)=[];         % Removes POI from list to avoid it from 
                                %  being the particle closest to itself
                                
    % Removes particles that are more than 1 cm away from the center of the
    %  the POI in the x and y directions
    loc(loc(:,6+index_factor)>(poi(6+index_factor)+1),:)=[];
    loc(loc(:,6+index_factor)<(poi(6+index_factor)-1),:)=[];
    loc(loc(:,7+index_factor)>(poi(7+index_factor)+1),:)=[];
    loc(loc(:,7+index_factor)<(poi(7+index_factor)-1),:)=[];
    
    if isempty(loc);
        
        index_list(mixing_particles(particle),2)=0; 
    
    else
        
        particle_list(particle)=1;
        
        % Creates the complex system of  POI location and other particles
        poi_compl=poi(6+index_factor)+1i*poi(7+index_factor);
        loc_compl=loc(:,6+index_factor)+1i*loc(:,7+index_factor);
        
        % Creates two matrices for comparing  distance for each particles
        % and the POI, then finds the particle that is closest to the POI
        [poipoi locloc] = meshgrid(poi_compl, loc_compl);
        distance=abs(poipoi-locloc);
        [min_distance min_index]=min(distance);
        neighbor=loc(min_index,1);
        
        % Record particle's neighbor number
        neighbors(particle)=neighbor;
        
        % Determines random particle for current particle
        random_particle=ceil(rand(1)*length(mixing_particles));
        % Records particle's random partner number
        randoms(particle)=mixing_particles(random_particle);
        
    end
    
end

mixing_particles=cat(2,mixing_particles,particle_list);
mixing_particles=mixing_particles(mixing_particles(:,end)>0,:);
neighbors=neighbors(neighbors(:)>0);
randoms=randoms(randoms(:)>0);
    

% Creates blank array to store the mixing index through time
Mixing_index=zeros(1,finaltime);
%test_random=zeros(1,finaltime);
%test_distance=zeros(1,finaltime);


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
    
    %vtpdata=cat(2,vtpdata,velocities);
    sorted=sortrows(vtpdata,1);
    sorted=cat(2,sorted,index_list(:,2));
    mixing_particles=sorted(sorted(:,end)>0,:);

    duo=cat(2,mixing_particles,neighbors);
    trio=cat(2,duo,randoms);   
    % Id diameter (density) U V W X Y Z NeighborId RandomId
    
    % Calculating numerator (neighbor distances)~~~~~~~~~~~~~~~~~~~~~~~~~~~
    % Calculates the distance between particles i and j, storing the value 
    %   in list neighbor_distances
    neighbor_distances=[];
    for i=1:length(mixing_particles)
        
        j=trio(i,end-1);
          
        dist=sqrt((mixing_particles(i,6+index_factor) - ...
            sorted(j,6+index_factor))^2 + ...
            (mixing_particles(i,7+index_factor) - ...
            sorted(j,7+index_factor))^2);
            
        neighbor_distances=cat(2,neighbor_distances,dist);
    end
    % Calculates the numerator for each timestep
    num=sum(neighbor_distances-diameter);
    
    %test_distance(timestep+1)=neighbor_distances(1500);
    
    % Calculating denominator (random distances)~~~~~~~~~~~~~~~~~~~~~~~~~~~
    % Calculates the distance between particles i and k, storing the value
    %    in list random_distances
    random_distances=[];
    for i=1:length(mixing_particles)
        
        k=trio(i,end);
        
        dist=sqrt((mixing_particles(i,6+index_factor) - ...
            sorted(k,6+index_factor))^2 + ...
            (mixing_particles(i,7+index_factor) - ...
            sorted(k,7+index_factor))^2);
        
        random_distances=cat(2,random_distances,dist);
    end
    % Calculates the denominator for each timestep
    denom=sum(random_distances-diameter);
            
    % Calculates the mixing index for the timestep~~~~~~~~~~~~~~~~~~~~~~~~~
    Mixing_index(timestep+1)=num/denom;
    
    % UNCOMMENT IF SAVING CSV FILES
%     csvwrite_with_headers([filename,'_mixing_particles.', ...
%         num2str(timestep), '.csv'], mixing_particles,headers,0,0);
    
end

plot(Mixing_index)

toc         %  Ends timing

cd('/home/jmschl/Desktop/MixingCalculations/')

csvwrite(['IND_',filename,'.csv'],Mixing_index);

cd('/home/jmschl/Repositories/magma')
