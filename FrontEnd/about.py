import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
#http://www.prepbootstrap.com/bootstrap-template/team-cards-flipper
#https://bootsnipp.com/snippets/92xNm
#<!-- Team member -->
def create_team_mate_card(name, photo, desc):
    team_card = dbc.Col( #<div class="col-xs-12 col-sm-6 col-md-4">
                    html.Div(#<div class="image-flip" >
                        html.Div([#<div class="mainflip flip-0">
                            html.Div(#<div class="frontside">
                                dbc.Card(#<div class="card">
                                    dbc.CardBody([#<div class="card-body text-center">
                                        html.P(#<p>
                                            html.Img(src=f"assets/img/{photo}", className=" img-fluid")#<img class=" img-fluid" src="https://sunlimetech.com/portfolio/boot4menu/assets/imgs/team/img_01.png" alt="card image">
                                        ),#</p>
                                        html.H4(name.upper(), className="card-title"),#<h4 class="card-title">Sunlimetech</h4>
                                        html.P(className="card-text"),#<p class="card-text">This is basic card with image on top, title, description and button.</p>
                                        #<a href="https://www.fiverr.com/share/qb8D02" class="btn btn-primary btn-sm"><i class="fa fa-plus"></i></a>
                                    ], className="card-body text-center"),#</div>
                                ),#</div>
                            className="frontside"),#</div>
                            html.Div(#<div class="backside">
                                dbc.Card(#<div class="card">
                                    dbc.CardBody([#<div class="card-body text-center mt-4">
                                        html.H4(name.upper(), className="card-title"),#<h4 class="card-title">Sunlimetech</h4>
                                        html.P(desc, className="card-text"),#<p class="card-text">This is basic card with image on top, title, description and button.This is basic card with image on top, title, description and button.This is basic card with image on top, title, description and button.</p>
                                        html.Ul([#<ul class="list-inline">
                                            html.Li(#<li class="list-inline-item">
                                                html.A(#<a class="social-icon text-xs-center" target="_blank" href="https://www.fiverr.com/share/qb8D02">
                                                    html.I(className="fa fa-facebook"),#<i class="fa fa-facebook"></i>
                                                className="social-icon text-xs-center", href="#foo"),#</a>
                                            className="list-inline-item"),#</li>
                                            html.Li(#<li class="list-inline-item">
                                                html.A(#<a class="social-icon text-xs-center" target="_blank" href="https://www.fiverr.com/share/qb8D02">
                                                    html.I(className="fa fa-twitter"),#<i class="fa fa-twitter"></i>
                                                className="social-icon text-xs-center", href="#foo"),#</a>
                                            className="list-inline-item"),#</li>
                                            html.Li(#<li class="list-inline-item">
                                                html.A(#<a class="social-icon text-xs-center" target="_blank" href="https://www.fiverr.com/share/qb8D02">
                                                    html.I(className="fa fa-skype"),#<i class="fa fa-skype"></i>
                                                className="social-icon text-xs-center", href="#foo"),#</a>
                                            className="list-inline-item"),#</li>
                                            html.Li(#<li class="list-inline-item">
                                                html.A(#<a class="social-icon text-xs-center" target="_blank" href="https://www.fiverr.com/share/qb8D02">
                                                    html.I(className="fa fa-google"),#<i class="fa fa-google"></i>
                                                className="social-icon text-xs-center", href="#foo"),#</a>
                                            className="list-inline-item"),#</li>
                                        ], className="list-inline"),#</ul>
                                    ]),#</div>
                                ),#</div>
                            className="backside"),#</div>
                        ],className="mainflip flip-0"),#</div>
                    className="image-flip" ),#</div>
                md=4,)#</div>
    return team_card

    
