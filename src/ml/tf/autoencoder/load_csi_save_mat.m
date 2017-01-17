clear;clc;

all_original_samples = [];
all_original_targets = [];
all_fuzhi_xiangwei_samples = [];
all_fuzhi_xiangwei_gudingyangben_samples = [];
all_fuzhi_xiangwei_gudingtongdao_samples = [];
all_fuzhi_xiangwei_targets = [];
%��36���������ת��mat��ʽ����
counter = 1;
for i = 1:6
    for j = 1:6
        read_file_name = ['l_' int2str(i) '.' int2str(j) '.csi'];
        try
            temp_data = csi_read(read_file_name, 'mat');
            %ȡʵ�����鲿���鲿������Ҫȡ��
            x = real(temp_data);
            x = x(1:180, :);
            y = -imag(temp_data);
            y = y(1:180, :);

            %���ֵ����λ
            fuzhi = sqrt(x .* x + y .* y);
            xiangwei = atan(y ./ x);
            %�޳���λ�к���NaN������
            original_size = size(xiangwei);
            new_size = size(xiangwei);
            jj = 1;
            while jj <= new_size(2)
                last_size = size(xiangwei);
                for ii = 1:original_size(1)
                    if isnan(xiangwei(ii,jj))
                        xiangwei(:, jj) = [];
                        fuzhi(:, jj) = [];
                        new_size = size(xiangwei);
                        break;
                    end
                end
                if new_size == last_size
                    jj = jj + 1;
                end
            end
            
            %�޳���Ĵ�С
            size_xiangwei = size(xiangwei);
            %�̶���һ����������λ��������������ֵ��������һ����������һ��������ͨ����λֵ��Ϊ0
            gudingyangben_xiangwei = zeros(size_xiangwei);
            for k  = 1:size_xiangwei(2)
                gudingyangben_xiangwei(:,k) = xiangwei(:,k) - xiangwei(:,1);
            end
            %�̶���һ��ͨ������λ������������������ͨ�����������Եĵ�һ��ͨ����ֵ��ÿ�������ĵ�һ��ͨ����λֵ��Ϊ0
            gudingtongdao_xiangwei = zeros(size_xiangwei);
            for g = 1:size_xiangwei(1)
                gudingtongdao_xiangwei(g,:) = xiangwei(g,:) - xiangwei(1,:);
            end
            
            %����ѵ��Ŀ��0/1����
            %��ʵ���鲿������Ӧ��
            size_x = size(x);
            temp_targets1 = zeros(36, size_x(2));
            temp_targets1(counter, :) = 1;
            %���޳���ķ�ֵ��λ��Ӧ��
            temp_targets2 = zeros(36, size_xiangwei(2));
            temp_targets2(counter, :) = 1;

            counter = counter + 1;
            %��������
            all_original_samples = [all_original_samples; [x', y']];
            all_original_targets = [all_original_targets; temp_targets1'];
            all_fuzhi_xiangwei_samples = [all_fuzhi_xiangwei_samples; [fuzhi', xiangwei']];
            all_fuzhi_xiangwei_gudingyangben_samples = [all_fuzhi_xiangwei_gudingyangben_samples; [fuzhi', gudingyangben_xiangwei']];
            all_fuzhi_xiangwei_gudingtongdao_samples = [all_fuzhi_xiangwei_gudingtongdao_samples; [fuzhi', gudingtongdao_xiangwei']];
            all_fuzhi_xiangwei_targets = [all_fuzhi_xiangwei_targets; temp_targets2'];
        catch
            fprintf('point %d.%d read error\n',i,j);
        end
    end
end
%��������
save('matfile/all_original_samples', 'all_original_samples');
save('matfile/all_original_targets', 'all_original_targets');
save('matfile/all_fuzhi_xiangwei_samples', 'all_fuzhi_xiangwei_samples');
save('matfile/all_fuzhi_xiangwei_gudingyangben_samples', 'all_fuzhi_xiangwei_gudingyangben_samples');
save('matfile/all_fuzhi_xiangwei_gudingtongdao_samples', 'all_fuzhi_xiangwei_gudingtongdao_samples');
save('matfile/all_fuzhi_xiangwei_targets', 'all_fuzhi_xiangwei_targets');
