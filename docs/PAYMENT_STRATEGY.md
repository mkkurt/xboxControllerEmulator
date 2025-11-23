# Payment Strategy: Why Gumroad?

You asked if Gumroad is the best option. For a solo developer selling a desktop app, the answer is **YES**. Here is why.

## The Options

| Feature | Gumroad | Stripe | Paddle | App Store |
| :--- | :--- | :--- | :--- | :--- |
| **Setup Time** | 15 Minutes | 2 Weeks | 3 Days | 1 Month |
| **Tax/VAT** | **Handled** ✅ | You do it ❌ | Handled ✅ | Handled ✅ |
| **Licensing** | **Built-in** ✅ | Build it yourself ❌ | Built-in ✅ | Built-in (DRM) |
| **Fee** | 10% + $0.30 | 2.9% + $0.30 | 5% + $0.50 | 15-30% |
| **Payout** | Weekly | Daily | Monthly | Monthly |

## Why Gumroad Wins for You

1.  **Merchant of Record (MoR):**
    *   **The Problem:** If you sell to a customer in Germany, you owe German VAT. If you sell to Japan, you owe Japanese tax.
    *   **Stripe:** You have to calculate, collect, and remit these taxes yourself. It is a nightmare.
    *   **Gumroad:** They act as the "reseller". They handle ALL global taxes. You just get paid.

2.  **Built-in Licensing:**
    *   Gumroad automatically generates a unique license key for every sale.
    *   They provide an API to verify it.
    *   **Stripe:** You would have to build your own database, key generator, and API server.

3.  **Speed:**
    *   We already have the product page text. You can be live in 10 minutes.
    *   Stripe requires building a checkout frontend.

## The Hybrid Strategy (Recommended)

Don't choose just one. Use the **Hybrid Model**:

1.  **Direct Sales (Gumroad):**
    *   For users who download from your website/Reddit/Discord.
    *   **Pros:** Fast updates, no review process, you get customer emails.
    *   **Security:** We implement Gumroad API verification.

2.  **App Store (Apple/Microsoft):**
    *   For users who want "safe" apps.
    *   **Pros:** Trust, discoverability.
    *   **Cons:** 30% fee, slow review process, sandboxing limits.

## Verdict
**Stick with Gumroad for the launch.**
It is the fastest way to validate your product and get paid without going to jail for tax evasion.
We can add the App Store later (Phase 3/4).
