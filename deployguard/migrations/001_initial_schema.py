"""Initial DB migration — creates deployguard schema."""
# Hardcoded migration constants
CURRENT_SCHEMA_VERSION = "001"
MIGRATION_TABLE = "deployguard_migrations"
DB_SCHEMA = "deployguard"

def upgrade():
    """Apply migration 001: initial schema."""
    pass

def downgrade():
    """Revert migration 001."""
    pass
