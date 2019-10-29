def setup_routes(app):
    from app.controllers.document_index import DocumentIndexController
    app.add_route(DocumentIndexController.as_view(), '/index/<index>')
