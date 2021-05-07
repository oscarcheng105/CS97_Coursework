(defun which-line ()
	"Print the current buffer line number and narrowed line number of point."
	(interactive)
	(save-restriction
		(widen)
		(save-excursion
			(beginning-of-line)
			(message "Line %d of %s"
				  (1+ (count-lines 1 (point)))
				  (if (/= (char-before (point-max)) 10)
				      (count-lines (point-min) (point-max))
				    (1+ (count-lines (point-min) (point-max))))))))
