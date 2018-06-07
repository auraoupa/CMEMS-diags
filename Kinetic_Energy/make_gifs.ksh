for name in NATL60_KEL_monthly_mean_coarse NATL60_KES_monthly_mean_coarse NATL60_KET_monthly_mean_coarse NATL60_ratio_KESover_KEL_monthly_mean_coarse NATL60_ratio_KESover_KET_monthly_mean_coarse; do

	convert -delay 120 -loop 0 ${name}_m*.png ${name}.gif

done

