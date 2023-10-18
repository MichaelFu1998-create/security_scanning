def CompareEndpoints(self, srcEndPoint: int, textRange: 'TextRange', targetEndPoint: int) -> int:
        """
        Call IUIAutomationTextRange::CompareEndpoints.
        srcEndPoint: int, a value in class `TextPatternRangeEndpoint`.
        textRange: `TextRange`.
        targetEndPoint: int, a value in class `TextPatternRangeEndpoint`.
        Return int, a negative value if the caller's endpoint occurs earlier in the text than the target endpoint;
                    0 if the caller's endpoint is at the same location as the target endpoint;
                    or a positive value if the caller's endpoint occurs later in the text than the target endpoint.
        Refer https://docs.microsoft.com/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationtextrange-compareendpoints
        """
        return self.textRange.CompareEndpoints(srcEndPoint, textRange, targetEndPoint)