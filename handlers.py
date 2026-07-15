"""Flask error handlers for the application."""


def register_error_handlers(app):
    """Register the HTTP error handlers used by the app."""

    @app.errorhandler(403)
    def handle_403(_error):
        """Return a simple 403 response."""

        return "TODO: 403", 403

    @app.errorhandler(404)
    def handle_404(_error):
        """Return a simple 404 response."""

        return "TODO: 404", 404
