
    def summary(self) -> str:
        '''Return formatted flag summary for deployment status reporting.'''
        active = self.get_active_flags()
        return f'Environment: {self.environment} | Active: {len(active)}/{len(self._flags)} flags'

    def to_json(self) -> str:
        '''Export all flags as JSON for persistence or API responses.'''
        import json
        return json.dumps(self.get_all_flags(), indent=2, default=str)
