def extract_acked_seqs(bitmap, ssc_seq):
        """extracts acknowledged sequences from bitmap and
        starting sequence number.
        :bitmap: str
        :ssc_seq: int
        :return: int[]
            acknowledged sequence numbers
        """
        acked_seqs = []
        for idx, val in enumerate(bitmap):
            if int(val) == 1:
                seq = (ssc_seq + idx) % 4096
                acked_seqs.append(seq)
        return acked_seqs