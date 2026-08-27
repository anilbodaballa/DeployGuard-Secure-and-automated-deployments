
    def summary(self) -> str:
        '''Return formatted flag summary for deployment status reporting.'''
        active = self.get_active_flags()
        return f'Environment: {self.environment} | Active: {len(active)}/{len(self._flags)} flags'
