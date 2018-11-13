"""
model.py file. Handles all the database connections and queries
"""
from db import db


class FeatureModel(db.Model):
    __tablename__ = "featureRequest"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    description = db.Column(db.Text)
    client = db.Column(db.String(100))
    client_priority = db.Column(db.Integer)
    target_date = db.Column(db.String(100))
    product_areas = db.Column(db.String(100))

    def __init__(self, title, description, client, client_priority, target_date, product_areas):
        """
         New instance function for instantiating the Class
        :param title:
        :param description:
        :param client:
        :param client_priority:
        :param target_date:
        :param product_areas:
        """
        self.title = title
        self.description = description
        self.client = client
        self.client_priority = client_priority
        self.target_date = target_date
        self.product_areas = product_areas

    def save(self):
        """
        Function to save new feature request into database. Functions queries the database to ensure there is no
        duplicate Client Priority set.

        If there is, it increments the priority of the old request by one and saves it back

        ALGORITHM
        result = get_data_from_database(where priority = new_priority)
        while Loop:
            if result is not None:
                increase priority by one
                check if new priority exists in the database
                save the old result with the new priority

                if new priority exists in the database
                    assign new data to old data

                commit changes to database
            else:
                break
        :return:
        """
        priority = self.client_priority
        #   Check if priority exists already for client for a different request
        result = self.query.filter_by(client_priority=priority, client=self.client).first()

        #   Start Loop
        while True:
            #   Check if result is empty. If empty Break
            if result is not None:
                #   result is not empty. increase priority by 1
                priority = int(priority) + 1

                #   check if the new priority exists in Database for the Client
                later_result = self.query.filter_by(client_priority=priority, client=self.client).first()

                #   Update result with new priority and save instance
                result.client_priority = priority
                db.session.commit()

                #   If new priority also exists for the Client, make result the new instance else break
                if later_result is not None:
                    result = later_result
                else:
                    break
            else:
                break

        #   Save the new session to Database
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def return_json(feature_request):
        """
            Model Function to turn a Feature Request Instance into a dict
        :param feature_request:
        :return: dict
        """
        return {
            'title': feature_request.title,
            'description': feature_request.description,
            'client': feature_request.client,
            'client_priority': feature_request.client_priority,
            'target_date': feature_request.target_date,
            'product_areas': feature_request.product_areas
        }

    @classmethod
    def find_by_name(cls, client_name):
        """
        Model Function to return a list of feature request made by a particular Client
        :param client_name:
        :return: list
        """
        feature_req = cls.query.filter_by(client=client_name).all()
        return list(cls.return_json(single_request) for single_request in feature_req)

    @classmethod
    def find_by_date(cls, query_date):
        """
        Model Function to return a list of feature request with a particular target date
        :param query_date:
        :return: list
        """
        feature_req = cls.query.filter_by(target_date=query_date).all()
        return list(cls.return_json(single_request) for single_request in feature_req)

    @classmethod
    def find_by_product(cls, query_product):
        """
        Model Function to return a list of  feature request made under a particular Product Area
        :param query_product:
        :return: list
        """
        feature_req = cls.query.filter_by(product_areas=query_product).all()
        return list(cls.return_json(single_request) for single_request in feature_req)

    @classmethod
    def return_all(cls):
        """
        Model Function to return list of all the feature requests in the database
        :return: list
        """
        all_request = cls.query.all()
        return list(cls.return_json(single_request) for single_request in all_request)
