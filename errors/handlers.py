"""Error handler pseudocode registration."""


def register_error_handlers(app):
    """Register HTTP error handlers to Flask app."""

    @app.errorhandler(403)
    def handle_403(_error):
        return "TODO: 403", 403

    @app.errorhandler(404)
    def handle_404(_error):
        return "TODO: 404", 404
