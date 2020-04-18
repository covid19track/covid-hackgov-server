from quart import Quart, request
from blueprints import hello_api
import config
import logbook
import sys

if __name__ == "__main__":
    handler = logbook.StreamHandler(sys.stdout, level=logbook.INFO)
    handler.push_application()

    log = logbook.Logger("covid_hackgov_server.boot")

    app = Quart(__name__)
    app.config.from_object(f"config.{config.MODE}")
    app.debug = app.config.get("DEBUG", False)

    if app.debug:
        handler.level = logbook.DEBUG
        app.logger.level = logbook.DEBUG
        log.debug("Running in debug mode")

    bps = {
        hello_api: None
    }

    for bp, suffix in bps.items():
        app.register_blueprint(bp.bp, url_prefix=f"/v1/{suffix or ''}")

    @app.after_request
    async def app_after_request(resp):
        """Handle CORS headers."""
        origin = request.headers.get("Origin", "*")
        resp.headers["Access-Control-Allow-Origin"] = origin
        resp.headers["Access-Control-Allow-Headers"] = (
            "*, X-Super-Properties, "
            "X-Fingerprint, "
            "X-Context-Properties, "
            "X-Failed-Requests, "
            "X-Debug-Options, "
            "Content-Type, "
            "Authorization, "
            "Origin, "
            "If-None-Match"
        )
        resp.headers["Access-Control-Allow-Methods"] = resp.headers.get("allow", "*")

        return resp

    app.run(port=app.config.get("PORT", 3000))