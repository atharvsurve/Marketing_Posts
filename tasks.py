from crewai import Task
from textwrap import dedent


class MarketingAnalysisTasks:

    def product_analysis(self, agent, product_website, product_details):
        return Task(
            description=dedent(f"""
                Analyze the given product website: {product_website}

                Extra details:
                {product_details}

                Focus on:
                - Product features
                - Brand positioning
                - Unique selling propositions
                - Customer pain points solved
                - Market appeal

                Provide suggestions for improving positioning and marketing.
            """),

            expected_output="""
            A detailed report containing:
            1. Brand overview
            2. Product strengths
            3. Unique selling points
            4. Target audience
            5. Market positioning
            6. Marketing recommendations
            """,

            agent=agent
        )

    def competitor_analysis(self, agent, product_website, product_details):
        return Task(
            description=dedent(f"""
                Analyze competitors of:

                {product_website}

                Additional details:
                {product_details}

                Identify the top 3 competitors and compare:

                - Branding
                - Social media strategy
                - Customer engagement
                - Strengths
                - Weaknesses
                - Marketing channels
            """),

            expected_output="""
            A competitor analysis report containing:

            - Top 3 competitors
            - Comparison table
            - Market positioning
            - Opportunities for differentiation
            - Strategic recommendations
            """,

            agent=agent
        )

    def campaign_development(self, agent, product_website, product_details):
        return Task(
            description=dedent(f"""
                Create a marketing campaign for:

                {product_website}

                Customer requirements:
                {product_details}

                Develop:

                - Campaign theme
                - Instagram strategy
                - Content pillars
                - Reels ideas
                - Visual identity
                - CTA ideas

                Focus on audience engagement and brand value.
            """),

            expected_output="""
            A complete marketing campaign including:

            - Campaign concept
            - Audience profile
            - Instagram strategy
            - Content ideas
            - Visual guidelines
            - CTA suggestions
            """,

            agent=agent
        )

    def instagram_ad_copy(self, agent):
        return Task(
            description=dedent("""
                Write engaging Instagram ad copies.

                Requirements:

                - Short and punchy
                - Emotional
                - Brand focused
                - Clear CTA
                - Suitable for Instagram
            """),

            expected_output="""
            3 Instagram ad copy options.

            Each should contain:
            - Hook
            - Main message
            - CTA
            - Relevant hashtags
            """,

            agent=agent
        )

    def take_photograph_task(
        self,
        agent,
        copy,
        product_website,
        product_details
    ):
        return Task(
            description=dedent(f"""
                You are creating a premium Instagram campaign.

                Product:
                {product_website}

                Details:
                {product_details}

                Ad Copy:
                {copy}

                Create three cinematic image prompts.

                Do NOT show the product directly.

                Focus on:
                - Luxury
                - Lifestyle
                - Emotion
                - Aspirational feeling
                - Professional photography
            """),

            expected_output="""
            3 image prompts.

            Each prompt should be:
            - One paragraph
            - Highly detailed
            - Cinematic
            - Suitable for Midjourney
            - Include lighting, composition and mood
            """,

            agent=agent
        )

    def review_photo(self, agent, product_website, product_details):
        return Task(
            description=dedent(f"""
                Review the generated image concepts.

                Product:
                {product_website}

                Additional details:
                {product_details}

                Evaluate:

                - Brand alignment
                - Emotional appeal
                - Luxury feel
                - Marketing effectiveness

                Improve descriptions if necessary.
            """),

            expected_output="""
            3 final approved image prompts.

            Each prompt should:
            - Be refined
            - Match the brand identity
            - Be ready for Midjourney generation
            """,

            agent=agent
        )