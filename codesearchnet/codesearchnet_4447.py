def get_data_manager(cls):
        """Return the DataManager of the currently loaded DataFlowKernel.
        """
        from parsl.dataflow.dflow import DataFlowKernelLoader
        dfk = DataFlowKernelLoader.dfk()

        return dfk.executors['data_manager']