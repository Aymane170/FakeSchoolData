{% macro debug_account() %}
    {{ log("Current account info:", info=True) }}
    {% set query %}
        SELECT 
            CURRENT_ACCOUNT() AS account,
            CURRENT_USER() AS user,
            CURRENT_ROLE() AS role,
            CURRENT_REGION() AS region
    {% endset %}

    {% set results = run_query(query) %}

    {% for row in results %}
        {{ log("Account: " ~ row['ACCOUNT'], info=True) }}
        {{ log("User: " ~ row['USER'], info=True) }}
        {{ log("Role: " ~ row['ROLE'], info=True) }}
        {{ log("Region: " ~ row['REGION'], info=True) }}
    {% endfor %}
{% endmacro %}
