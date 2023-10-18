def __deal_with_pagination(self, url, method, params, data):
        """
            Perform multiple calls in order to have a full list of elements
            when the API are "paginated". (content list is divided in more
            than one page)
        """
        all_data = data
        while data.get("links", {}).get("pages", {}).get("next"):
            url, query = data["links"]["pages"]["next"].split("?", 1)

            # Merge the query parameters
            for key, value in urlparse.parse_qs(query).items():
                params[key] = value

            data = self.__perform_request(url, method, params).json()

            # Merge the dictionaries
            for key, value in data.items():
                if isinstance(value, list) and key in all_data:
                    all_data[key] += value
                else:
                    all_data[key] = value

        return all_data