class ReadReplicaRouter:
    def db_for_read(self, model, **hints):
        """Direct read queries to the 'read' database."""
        return "read"

    def db_for_write(self, model, **hints):
        """Direct write queries to the 'default' database."""
        return "default"

    def allow_relation(self, obj1, obj2, **hints):
        """Allow relationships if both objects are in the same database."""
        db_set = {"read", "default"}
        if obj1._state.db in db_set and obj2._state.db in db_set:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """Ensure all migrations are applied only to the default (write) database."""
        return db == "default"
