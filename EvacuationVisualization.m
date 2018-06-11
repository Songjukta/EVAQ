env = csvread('Environment_States.csv');
% grid size
x_grid = 10; y_grid = 10;

%env(y_grid+1:y_grid+1:size(env,1),:) = [];
num_step = size(env,1)/x_grid;
M = cell(num_step,1);
for k = 1:num_step
    M{k,1} = env((k-1)*y_grid+1:k*y_grid,:);
end

% Color Map:
cMap = [0.75,0.75,0.75;1,1,1;1,0.65,0;1,0.85,0;1,0,0;0,1,0];

v = VideoWriter(['animation_',datestr(now,'mmddyyyy_HHMM'),'.mp4'],'MPEG-4');
v.FrameRate = 30;
open(v);

for k = 1:num_step
    m = M{k,1};
    disp(k);
    
    transition_frames = 15;
    for trans = 1:transition_frames
        
        % Draw Rectangles
        f = figure;
        h = axes;
        
        % Time Steps
        rectangle('Position',[0,-2,x_grid,2],'FaceColor',[0,0,0],'EdgeColor','k'); hold on;
        text(x_grid/2,-1,['Time Step: ', num2str(k)],'HorizontalAlignment','center','Color', [1,1,1],'FontSize',10);
        
        % Draw Legends
        rectangle('Position',[x_grid,-2,10,y_grid+2],'FaceColor',[1,1,1],'EdgeColor','k'); hold on;
        legends = {'Cell not accessible','Cell accessible','Regular exit','Special exit','Hazard','Agent'};
        for i = 1:6
            rectangle('Position',[x_grid+1,y_grid-8+i,1,1],'FaceColor',cMap(i,:),'EdgeColor','k');
            text(x_grid+2.5,y_grid-8+i+0.5,legends{1,i},'HorizontalAlignment','left','FontSize',8);
        end
        
        % Draw the exits
        for i = 1:size(m,1)
            for j = 1:size(m,2)
                if M{1,1}(i,j) == 2 || M{1,1}(i,j) == 3
                    rectangle('Position',[j-1,i-1,1,1],'FaceColor',cMap(M{1,1}(i,j)+1,:),'EdgeColor','none'); 
                    hold on;
                end
            end
        end
        
        for i = 1:size(m,1)
            for j = 1:size(m,2)
                if m(i,j) ~= 1 && m(i,j) ~= 2 && m(i,j) ~= 3
                    if m(i,j)>4
                        x = j; y = i;
                        
                        % Arrow for moving direction
                        if k ~= 1 && k ~= num_step
                            [p,q] = find(M{k+1,1}==m(i,j));
                            if ~isempty(p)
                                x = j+(q-j)*(trans-1)/transition_frames; 
                                y = i+(p-i)*(trans-1)/transition_frames; 
                                line([x,q]-0.5,[y,p]-0.5,'Color','b','LineWidth',1); hold on;
                                rectangle('Position',[q-0.625,p-0.625,0.25,0.25],'FaceColor','b','EdgeColor','none','Curvature',1);
                            end
                            [a,b] = find(M{k-1,1}==m(i,j));
                            if ~isempty(a)
                                line([x,b]-0.5,[y,a]-0.5,'Color','r','LineWidth',0.1); hold on;
                                rectangle('Position',[b-0.55,a-0.55,0.1,0.1],'FaceColor','r','EdgeColor','none','Curvature',1);
                            end
                        end
                        
                        % Draw Agents
                        rectangle('Position',[x-0.95,y-0.95,0.9,0.9],'FaceColor',cMap(6,:),...
                            'EdgeColor',[0,0,0],'Curvature',1); 
                        hold on;
                        text(x-0.5,y-0.5,num2str(m(i,j)),'HorizontalAlignment','center','FontSize',6);

                    else
                        rectangle('Position',[j-1,i-1,1,1],'FaceColor',cMap(m(i,j)+1,:),'EdgeColor','none'); 
                        hold on;
                    end
                end
            end
        end
        
        % Flash
        if trans == transition_frames
            rectangle('Position',[0,-2,20,2],'FaceColor',[1,1,1],'EdgeColor','k'); hold on;
        end
        
        set(gca,'xtick', linspace(0,x_grid,x_grid+1), 'ytick', linspace(0,y_grid,y_grid+1));
        set(gca,'xgrid', 'on', 'ygrid', 'on', 'gridlinestyle', '-', 'xcolor', 'k', 'ycolor', 'k');    
        set(h, 'Ydir', 'reverse'); daspect([1 1 1]);
        xlim([0, x_grid+10]); ylim([-2, y_grid]);
        frame = getframe;
        writeVideo(v,frame);
        close(f);
    end
end

close(v);