def splitext_files_only(filepath):
	"Custom version of splitext that doesn't perform splitext on directories"
	return (
		(filepath, '') if os.path.isdir(filepath) else os.path.splitext(filepath)
	)