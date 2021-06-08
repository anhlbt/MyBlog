<template>
    <div>
        <b-container>
            <b-row>
                    <b-col cols="12" md="6" v-if="agentsIndex < agents.length" v-for="agentsIndex in agentsToShow" :key="agentsIndex.id">
                        <div class="agent-card">
                            <div class="profile-card-img"><img src="@/assets/images/agent.png" alt=""></div>
                            <div class="agent-name">{{agents[agentsIndex].name}} </div>
                            <div class="agent-numbers">
                                <div class="single-number">
                                    <p>{{agents[agentsIndex].rent}}</p>
                                    <div class="number-description">Rent Properties</div>
                                </div>
                                
                                 <div class="single-number">
                                    <p>{{agents[agentsIndex].sale}}</p>
                                    <div class="number-description">Sale Properties</div>
                                </div>

                                 <div class="single-number">
                                    <p>{{agents[agentsIndex].reviews}}</p>
                                    <div class="number-description">Reviews</div>
                                </div>

                                 <div class="single-number">
                                    <p>{{agents[agentsIndex].experience}}</p>
                                    <div class="number-description">Experience</div>
                                </div>
                            </div>

                            <div class="agent-social">
                                <a href="#" class="agent-social-icon facebook"><div class="fa fa-facebook"></div></a>
                                <a href="#" class="agent-social-icon instagram"><div class="fa fa-instagram"></div></a>
                                <a href="#" class="agent-social-icon twitter"><div class="fa fa-twitter"></div></a>
                                <a href="#" class="agent-social-icon linkedin"><div class="fa fa-linkedin"></div></a>
                            </div>
                            
                        </div>
                           
                    </b-col>
                    <div class="agents-buttons">
                        <div v-if="agentsToShow < agents.length">
                        <b-button class="btn-outline-style1" @click="agentsToShow += 2">Show more agents</b-button>
                        </div>
                        <div v-if="agentsToShow < agents.length && agentsToShow > 2 || agentsToShow >= agents.length">
                            <b-button class="btn-outline-style1" @click="agentsToShow -= 2">Show less agents</b-button>
                        </div>
                        <div v-if="agentsToShow >= agents.length">
                            <a href="#" class="show-agents-btn" >Show all agents</a>
                        </div>
                    </div>
            </b-row>
        </b-container>
        
        </div>
</template>

<script>
    export default {
        data() {
            return {
                agentsToShow: 2,
                totalAgents: 0,
                agents: [
                    {
                        name: "Anhlbt",
                        img: "@/assets/images/agent.png",
                        email: "paul@realestate.com",
                        phone: "+407222333",
                        experienceBadge: "Best experience",
                        reviewsBadge: "Best reviews",
                        rent: "125",
                        sale: "42",
                        reviews: "85",
                        experience: "5 years",
                    },
                     {
                        name: "Anhlbt",
                        img: "_nuxt/assets/images/placeholder.jpg",
                        email: "paul@realestate.com",
                        phone: "+407222333",
                        experience: "Best experience",
                        reviews: "Best reviews",
                        rent: "125",
                        sale: "42",
                        reviews: "85",
                        experience: "5 years",
                    },
                     {
                        name: "Anhlbt",
                        img: "_nuxt/assets/images/placeholder.jpg",
                        email: "paul@realestate.com",
                        phone: "+407222333",
                        experience: "Best experience",
                        reviews: "Best reviews",
                        rent: "125",
                        sale: "42",
                        reviews: "85",
                        experience: "5 years",
                    },
                     {
                        name: "Anhlbt",
                        img: "_nuxt/assets/images/placeholder.jpg",
                        email: "paul@realestate.com",
                        phone: "+407222333",
                        experience: "Best experience",
                        reviews: "Best reviews",
                        rent: "125",
                        sale: "42",
                        reviews: "85",
                        experience: "5 years",
                    },
                     {
                        name: "Anhlbt",
                        img: "_nuxt/assets/images/placeholder.jpg",
                        email: "paul@realestate.com",
                        phone: "+407222333",
                        experience: "Best experience",
                        reviews: "Best reviews",
                        rent: "125",
                        sale: "42",
                        reviews: "85",
                        experience: "5 years",
                    },
                     {
                        name: "Anhlbt",
                        img: "_nuxt/assets/images/placeholder.jpg",
                        email: "paul@realestate.com",
                        phone: "+407222333",
                        experience: "Best experience",
                        reviews: "Best reviews",
                        rent: "125",
                        sale: "42",
                        reviews: "85",
                        experience: "5 years",
                    },
                     {
                        name: "Anhlbt",
                        img: "_nuxt/assets/images/placeholder.jpg",
                        email: "paul@realestate.com",
                        phone: "+407222333",
                        experience: "Best experience",
                        reviews: "Best reviews",
                        rent: "125",
                        sale: "42",
                        reviews: "85",
                        experience: "5 years",
                    },
                    {
                        name: "Anhlbt",
                        img: "_nuxt/assets/images/placeholder.jpg",
                        email: "paul@realestate.com",
                        phone: "+407222333",
                        experience: "Best experience",
                        reviews: "Best reviews",
                        rent: "125",
                        sale: "42",
                        reviews: "85",
                        experience: "5 years",
                    },
                ],
            };
        },
        mounted() {
            this.totalAgents = this.agents.length
            
        }
    }
</script>

<style lang="scss" scoped>
@import "./../../assets/scss/_variables";
    .agent-card {
        margin: 60px 0;
        .profile-card-img img{
            width: 150px;
            height: 150px;
            margin-left: auto;
            margin-right: auto;
            transform: translateY(-50%);
            border-radius: 50%;
            overflow: hidden;
            position: relative;
            z-index: 4;
            box-shadow: 0px 5px 50px 0px $color1, 0px 0px 0px 7px $color1-light;
        }

        .agent-name {
            font-weight: 700;
            font-size: 24px;
            color: $color1;
            margin-bottom: 15px;
        }

        .agent-numbers {
            display: flex;

            .single-number {
                flex: 1;
                
                p {
                    font-weight: 700;
                    font-size: 22px;
                    color: #324e63;
                    margin-bottom: 0;
                }

                .number-description {
                    font-weight: 300;
                    font-size: 12px;
                    color: #000;
                }
            }
        }

        .agent-social {
            display: flex;
            justify-content: center;
            align-content: center;

            .agent-social-icon {
                display: inline-flex;
                width: 55px;
                height: 55px;
                margin: 15px;
                border-radius: 50%;
                align-items: center;
                justify-content: center;
                color: #fff;
                background: #405de6;
                box-shadow: 0px 7px 30px rgba(43, 98, 169, 0.5);
                position: relative;
                font-size: 21px;
                flex-shrink: 0;
                transition: all .6s;

                &:hover {
                    text-decoration: none;
                    transform: rotateY(180deg);
                    -moz-transform: rotateY(180deg);
                    -webkit-transform: rotateY(180deg);
                }
            }

            .facebook {
                background: linear-gradient(45deg, #3b5998, #0078d7);
                box-shadow: 0px 4px 30px rgba(43, 98, 169, 0.5);
            }

            .twitter {
                background: linear-gradient(45deg, #1da1f2, #0e71c8);
                box-shadow: 0px 4px 30px rgba(19, 127, 212, 0.7);
            }

            .instagram {
                background: linear-gradient(45deg, #405de6, #5851db, #833ab4, #c13584, #e1306c, #fd1d1d);
                box-shadow: 0px 4px 30px rgba(120, 64, 190, 0.6);
            }

            .linkedin {
                background: linear-gradient(45deg, #324e63, #414447);
                box-shadow: 0px 4px 30px rgba(55, 75, 90, 0.6);
            }
        }
    }

    .agents-buttons {
    display: flex;
    justify-content: center;
    width: 100%;

    button {
        margin: 0 20px;
    }

    .show-agents-btn {
        background: $gradient1;
        color: #fff;
        padding: 12px 35px;
        border-radius: 30px;
        text-transform: uppercase;
        text-decoration: none;
        box-shadow: 0 6px 12px 0 rgba(38, 54, 128, 0.2);
        -webkit-box-shadow: 0 6px 12px 0 rgba(38, 54, 128, 0.2);
        -moz-box-shadow: 0 6px 12px 0 rgba(38, 54, 128, 0.2);
    }
    }
</style>