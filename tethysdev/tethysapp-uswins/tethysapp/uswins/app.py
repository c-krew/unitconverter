from tethys_sdk.base import TethysAppBase, url_map_maker


class Uswins(TethysAppBase):
    """
    Tethys app class for US Wins.
    """

    name = 'US Wins'
    index = 'uswins:home'
    icon = 'uswins/images/icon.gif'
    package = 'uswins'
    root_url = 'uswins'
    color = '#f39c12'
    description = 'Place a brief description of your app here.'
    tags = ''
    enable_feedback = False
    feedback_emails = []

    def url_maps(self):
        """
        Add controllers
        """
        UrlMap = url_map_maker(self.root_url)

        url_maps = (
            UrlMap(
                name='home',
                url='uswins',
                controller='uswins.controllers.home'
            ),
            UrlMap(
                name='scores',
                url='uswins/scores',
                controller='uswins.controllers.scores'
            ),
            UrlMap(
                name='about',
                url='uswins/about',
                controller='uswins.controllers.about'
            ),
            UrlMap(
                name='forecastpercent',
                url='uswins/forecastpercent',
                controller='uswins.ajax_controllers.forecastpercent'
            ),
        )

        return url_maps
