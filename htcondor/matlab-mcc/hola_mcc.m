
fixed_nii_file = '/opt/myapp/workdir/chris_t1.nii.gz';
moving_nii_file = '/opt/myapp/workdir/chris_t2.nii.gz';
output_nii_file = '/opt/myapp/workdir/output.nii.gz';

fixed_info = niftiinfo(fixed_nii_file);
volfix = niftiread(fixed_info);

moving_info = niftiinfo(moving_nii_file);
volmov = niftiread(moving_info);

spc = fixed_info.PixelDimensions;
% configure registration
opts = [];
opts.k_down = 0.7;
opts.interp_type = 0;
opts.metric = 'loc_cc_fftn_gpu';
opts.metric_param = [1,1,1] * 2.1;
opts.scale_metric_param = true;
opts.isoTV = 0.11;
opts.csqrt = 5e-3;
opts.spline_order = 1;
opts.border_mask = 5;
opts.max_iters = 2;
opts.check_gradients = 100*0;
opts.pix_resolution = spc;

[voldef, Tptv, Kptv] = ptv_register(volmov, volfix, opts);

fixed_info.Datatype = 'double';
fixed_info.BitsPerPixel = 64;
niftiwrite(voldef,output_nii_file,fixed_info);