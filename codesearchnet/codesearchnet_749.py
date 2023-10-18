def moses_multi_bleu(hypotheses, references, lowercase=False):
    """Calculate the bleu score for hypotheses and references
    using the MOSES ulti-bleu.perl script.

    Parameters
    ------------
    hypotheses : numpy.array.string
        A numpy array of strings where each string is a single example.
    references : numpy.array.string
        A numpy array of strings where each string is a single example.
    lowercase : boolean
        If True, pass the "-lc" flag to the multi-bleu script

    Examples
    ---------
    >>> hypotheses = ["a bird is flying on the sky"]
    >>> references = ["two birds are flying on the sky", "a bird is on the top of the tree", "an airplane is on the sky",]
    >>> score = tl.nlp.moses_multi_bleu(hypotheses, references)

    Returns
    --------
    float
        The BLEU score

    References
    ----------
    - `Google/seq2seq/metric/bleu <https://github.com/google/seq2seq>`__

    """
    if np.size(hypotheses) == 0:
        return np.float32(0.0)

    # Get MOSES multi-bleu script
    try:
        multi_bleu_path, _ = urllib.request.urlretrieve(
            "https://raw.githubusercontent.com/moses-smt/mosesdecoder/"
            "master/scripts/generic/multi-bleu.perl"
        )
        os.chmod(multi_bleu_path, 0o755)
    except Exception:  # pylint: disable=W0702
        tl.logging.info("Unable to fetch multi-bleu.perl script, using local.")
        metrics_dir = os.path.dirname(os.path.realpath(__file__))
        bin_dir = os.path.abspath(os.path.join(metrics_dir, "..", "..", "bin"))
        multi_bleu_path = os.path.join(bin_dir, "tools/multi-bleu.perl")

    # Dump hypotheses and references to tempfiles
    hypothesis_file = tempfile.NamedTemporaryFile()
    hypothesis_file.write("\n".join(hypotheses).encode("utf-8"))
    hypothesis_file.write(b"\n")
    hypothesis_file.flush()
    reference_file = tempfile.NamedTemporaryFile()
    reference_file.write("\n".join(references).encode("utf-8"))
    reference_file.write(b"\n")
    reference_file.flush()

    # Calculate BLEU using multi-bleu script
    with open(hypothesis_file.name, "r") as read_pred:
        bleu_cmd = [multi_bleu_path]
        if lowercase:
            bleu_cmd += ["-lc"]
        bleu_cmd += [reference_file.name]
        try:
            bleu_out = subprocess.check_output(bleu_cmd, stdin=read_pred, stderr=subprocess.STDOUT)
            bleu_out = bleu_out.decode("utf-8")
            bleu_score = re.search(r"BLEU = (.+?),", bleu_out).group(1)
            bleu_score = float(bleu_score)
        except subprocess.CalledProcessError as error:
            if error.output is not None:
                tl.logging.warning("multi-bleu.perl script returned non-zero exit code")
                tl.logging.warning(error.output)
            bleu_score = np.float32(0.0)

    # Close temp files
    hypothesis_file.close()
    reference_file.close()

    return np.float32(bleu_score)