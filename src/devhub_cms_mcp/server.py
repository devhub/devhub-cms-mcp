import json
import os
from urllib.parse import urlparse

from mcp.server.fastmcp import FastMCP
from requests_oauthlib import OAuth1Session


# Initialize FastMCP server
mcp = FastMCP(
    "DevHub CMS MCP",
    description="Integration with DevHub CMS to manage content")


def get_client():
    """Get DevHub API client and base_url."""
    client = OAuth1Session(
        os.environ['DEVHUB_API_KEY'],
        client_secret=os.environ['DEVHUB_API_SECRET'])
    base_url = '{}/api/v2/'.format(os.environ['DEVHUB_BASE_URL'])
    return client, base_url


@mcp.tool()
def get_hours_of_operation(location_id: int, hours_type: str = 'primary') -> list:
    """Get the hours of operation for a DevHub location

    Returns a list of items representing days of the week

    Except for the special case formatting, this object is a list of 7 items which represent each day.

    Each day can can have one-four time ranges. For example, two time ranges denotes a "lunch-break". No time ranges denotes closed.

    Examples:
    9am-5pm [["09:00:00", "17:00:00"]]
    9am-12pm and 1pm-5pm [["09:00:00", "12:00:00"], ["13:00:00", "17:00:00"]]
    Closed - an empty list []

    Args:
        location_id: DevHub Location ID
        hours_type: Defaults to 'primary' unless the user specifies a different type
    """
    client, base_url = get_client()
    r = client.get('{}locations/{}'.format(base_url, location_id))
    content = json.loads(r.content)
    return content['hours_by_type'].get(hours_type, [])


@mcp.tool()
def get_businesses() -> list:
    """Get all businesses within the DevHub account

    Returns a list of businesses with the following fields:
    - id: Business ID that can be used in the other tools
    - business_name: Business name

    If only one business exists in the account, you can assume that the user wants to use that business for any business_id related tools.
    """
    client, base_url = get_client()
    params = {
        'deleted': 0,
        'limit': 20,
        'order_by': 'business_name',
        'project_type': 'default',
    }
    r = client.get('{}businesses/'.format(base_url), params=params)
    content = json.loads(r.content)
    return content['objects']


@mcp.tool()
def get_locations(business_id: int) -> list:
    """Get all locations for a business

    Returns a list of locations with the following fields:
    - id: Location ID that can be used in the other tools
    - location_name: Location name
    - location_url: Location URL in DevHub
    - street: Street address
    - city: City
    - state: State
    - country: Country
    - postal_code: Postal code
    - lat: Latitude
    - lon: Longitude
    """
    client, base_url = get_client()
    params = {
        'business_id': business_id,
        'limit': 600,
        'order_by': 'location_name',
    }
    r = client.get('{}locations/'.format(base_url), params=params)
    content = json.loads(r.content)
    return [{
        'id': location['id'],
        'location_name': location['location_name'],
        'location_url': location['location_url'],
        'street': location['street'],
        'city': location['city'],
        'state': location['state'],
        'country': location['country'],
        'postal_code': location['postal_code'],
        'lat': location['lat'],
        'lon': location['lon'],
    } for location in content['objects']]


@mcp.tool()
def update_hours(location_id: int, new_hours: list, hours_type: str = 'primary') -> str:
    """Update the hours of operation for a DevHub location

    Send a list of items representing days of the week

    Except for the special case formatting, this object is a list of 7 items which represent each day.

    Each day can can have one-four time ranges. For example, two time ranges denotes a "lunch-break". No time ranges denotes closed.

    Examples:
    9am-5pm [["09:00:00", "17:00:00"]]
    9am-12pm and 1pm-5pm [["09:00:00", "12:00:00"], ["13:00:00", "17:00:00"]]
    Closed - an empty list []

    Args:
        location_id: DevHub Location ID
        new_hours: Structured format of the new hours
        hours_type: Defaults to 'primary' unless the user specifies a different type
    """
    client, base_url = get_client()
    r = client.put(
        '{}locations/{}/'.format(base_url, location_id),
        json={
            'hours': [
                {
                    'type': hours_type,
                    'hours': new_hours,
                }
            ]
        },
    )
    content = json.loads(r.content)
    return 'Updated successfully'


@mcp.tool()
def site_from_url(url: str) -> str:
    """Get the DevHub site ID from a URL.

    Can prompt the user for the URL instead of passing a site_id.

    Returns details about the Site matches the URL that can be used in the other tools.
    - Site ID: ID of the DevHub site
    - Site URL: URL of the DevHub site
    - Site Location IDs: List of location IDs associated with the site

    Args:
        url: URL of the DevHub site, all lowercase and ends with a slash
    """
    parsed_url = urlparse(url)
    subdomain = parsed_url.netloc.split('.', 1)[0] or 'www'
    domain = parsed_url.netloc.split('.', 1)[1]
    base_directory = parsed_url.path
    client, base_url = get_client()
    r = client.get('{}sites/'.format(base_url), params={
        'base_directory': base_directory,
        'deleted': 0,
        'domain': domain,
        'subdomain': subdomain,
    })
    content = json.loads(r.content)
    if len(content['objects']) == 0:
        return 'No site found'
    site = content['objects'][0]
    return f"""
Site ID: {site['id']}
Site URL: {site['formatted_url']}
Site Location IDs: {", ".join([str(location_id) for location_id in site['location_ids']])}
"""


@mcp.tool()
def upload_image(base64_image_content: str, filename: str) -> str:
    """Upload an image to the DevHub media gallery

    Supports webp, jpeg and png images

    Args:
        base64_image_content: Base 64 encoded content of the image file
        filename: Filename including the extension
    """
    client, base_url = get_client()
    payload = {
        'type': 'image',
        'upload': {
            'file': base64_image_content,
            'filename': filename,
        }
    }
    r = client.post(
        '{}images/'.format(base_url),
        json=payload,
    )
    image = r.json()
    return f"""
Image ID: {image['id']}
Image Path (for use in HTML src attributes): {image['absolute_path']}
"""


@mcp.tool()
def get_blog_post(post_id: int) -> str:
    """Get a single blog post

    Args:
        post_id: Blog post id
    """
    client, base_url = get_client()
    r = client.get('{}posts/{}/'.format(base_url, post_id))
    post = r.json()
    return f"""
Post ID: {post['id']}
Title: {post['title']}
Date: {post['date']}

Content (HTML):
{post['content']}
"""


@mcp.tool()
def create_blog_post(site_id: int, title: str, content: str) -> str:
    """Create a new blog post

    Args:
        site_id: Website ID where the post will be published. Prompt the user for this ID.
        title: Blog post title
        content: HTML content of blog post. Should not include a <h1> tag, only h2+
    """
    client, base_url = get_client()
    payload = {
        'content': content,
        'site_id': site_id,
        'title': title,
    }
    r = client.post(
        '{}posts/'.format(base_url),
        json=payload,
    )
    post = r.json()
    return f"""
Post ID: {post['id']}
Title: {post['title']}
Date: {post['date']}

Content (HTML):
{post['content']}
"""


@mcp.tool()
def update_blog_post(post_id: int, title: str = None, content: str = None) -> str:
    """Update a single blog post

    Args:
        post_id: Blog post ID
        title: Blog post title
        content: HTML content of blog post. Should not include a <h1> tag, only h2+
    """
    client, base_url = get_client()
    payload = {}
    if content:
        payload['content'] = content
    if title:
        payload['title'] = title
    r = client.put(
        '{}posts/{}/'.format(base_url, post_id),
        json=payload,
    )
    post = r.json()
    return f"""
Post ID: {post['id']}
Title: {post['title']}
Date: {post['date']}

Content (HTML):
{post['content']}
"""


@mcp.tool()
def get_nearest_location(business_id: int, latitude: float, longitude: float) -> str:
    """Get the nearest DevHub location

    Args:
        business_id: DevHub Business ID associated with the location. Prompt the user for this ID
        latitude: Latitude of the location
        longitude: Longitude of the location
    """
    client, base_url = get_client()
    r = client.get('{}locations/'.format(base_url), params={
        'business_id': business_id,
        'near_lat': latitude,
        'near_lon': longitude,
    })
    objects = json.loads(r.content)['objects']
    if objects:
        return f"""
Location ID: {objects[0]['id']}
Location name: {objects[0]['location_name']}
Location url: {objects[0]['location_url']}
Street: {objects[0]['street']}
City: {objects[0]['city']}
State: {objects[0]['state']}
Country: {objects[0]['country']}
"""


def main():
    """Run the MCP server"""
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()
