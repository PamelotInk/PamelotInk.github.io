"""
Automated email notifications for experiment results.
Checks for significant experiments and sends email alerts.
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os

from core.data_manager import ExperimentDataManager
from core.statistical_engine import ABTestCalculator


# Email configuration - UPDATE THESE WITH YOUR SETTINGS
EMAIL_CONFIG = {
    'smtp_server': 'smtp.gmail.com',  # For Gmail
    'smtp_port': 587,
    'sender_email': 'pamtekk@gmail.com',  # Your email
    'sender_password': 'your_app_password',  # App password (not regular password)
    'recipient_email': 'pamtekk@gmail.com',  # Where to send results
}


def send_email(subject: str, body_html: str):
    """Send an email notification"""
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = EMAIL_CONFIG['sender_email']
    msg['To'] = EMAIL_CONFIG['recipient_email']
    
    html_part = MIMEText(body_html, 'html')
    msg.attach(html_part)
    
    try:
        with smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port']) as server:
            server.starttls()
            server.login(EMAIL_CONFIG['sender_email'], EMAIL_CONFIG['sender_password'])
            server.send_message(msg)
        print(f"✅ Email sent: {subject}")
        return True
    except Exception as e:
        print(f"❌ Email failed: {e}")
        return False


def check_and_notify():
    """Check experiments and send notifications for significant results"""
    dm = ExperimentDataManager()
    calc = ABTestCalculator()
    
    print(f"\n🔍 Checking experiments at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    active_exps = dm.get_active_experiments()
    
    if len(active_exps) == 0:
        print("No active experiments found.")
        return
    
    notifications = []
    
    for idx, exp in active_exps.iterrows():
        results_df = dm.get_experiment_results(exp['experiment_id'])
        
        if len(results_df) >= 2 and results_df['total_impressions'].sum() > 0:
            control = results_df[results_df['variant_name'] == 'control'].iloc[0]
            variant = results_df[results_df['variant_name'] != 'control'].iloc[0]
            
            if control['total_impressions'] > 0 and variant['total_impressions'] > 0:
                stats = calc.is_significant(
                    control_conv=int(control['total_conversions']),
                    control_imp=int(control['total_impressions']),
                    variant_conv=int(variant['total_conversions']),
                    variant_imp=int(variant['total_impressions'])
                )
                
                if stats['is_significant']:
                    notifications.append({
                        'experiment': exp['experiment_name'],
                        'exp_id': exp['experiment_id'],
                        'stats': stats,
                        'control': control,
                        'variant': variant
                    })
                    print(f"📊 {exp['experiment_name']}: Significant result found!")
    
    if notifications:
        send_results_email(notifications)
    else:
        print("No significant results to report yet.")


def send_results_email(notifications: list):
    """Format and send results email"""
    
    # Build HTML email
    html = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; }}
            .header {{ background-color: #4CAF50; color: white; padding: 20px; text-align: center; }}
            .experiment {{ border: 1px solid #ddd; margin: 20px; padding: 20px; border-radius: 5px; }}
            .metric {{ display: inline-block; margin: 10px; padding: 10px; background: #f5f5f5; border-radius: 5px; }}
            .winner {{ color: #4CAF50; font-weight: bold; font-size: 24px; }}
            .stats {{ background: #e3f2fd; padding: 15px; margin: 10px 0; border-radius: 5px; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🎉 Experiment Results Ready!</h1>
            <p>Significant results detected at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
    """
    
    for notif in notifications:
        stats = notif['stats']
        exp_name = notif['experiment']
        
        html += f"""
        <div class="experiment">
            <h2>{exp_name}</h2>
            <p class="winner">{'✅ WINNER DETECTED!' if stats['winner'] == 'variant' else '📊 Significant Result'}</p>
            
            <div class="stats">
                <div class="metric">
                    <strong>Control Rate:</strong><br>
                    {stats['control_rate']:.2f}%
                </div>
                <div class="metric">
                    <strong>Variant Rate:</strong><br>
                    {stats['variant_rate']:.2f}%
                </div>
                <div class="metric">
                    <strong>Lift:</strong><br>
                    {stats['relative_lift']:.1f}%
                </div>
                <div class="metric">
                    <strong>Confidence:</strong><br>
                    {stats['confidence']:.1f}%
                </div>
            </div>
            
            <p><strong>Sample Size:</strong></p>
            <ul>
                <li>Control: {int(notif['control']['total_impressions']):,} impressions, {int(notif['control']['total_conversions']):,} conversions</li>
                <li>Variant: {int(notif['variant']['total_impressions']):,} impressions, {int(notif['variant']['total_conversions']):,} conversions</li>
            </ul>
            
            <p><strong>Recommendation:</strong> 
            {'🚀 Ship the variant immediately!' if stats['winner'] == 'variant' else '⚠️ Keep current version or investigate further.'}
            </p>
            
            <p><a href="http://localhost:8501">View in Dashboard →</a></p>
        </div>
        """
    
    html += """
    </body>
    </html>
    """
    
    subject = f"🎯 {len(notifications)} Experiment{'s' if len(notifications) > 1 else ''} Ready for Review"
    send_email(subject, html)


if __name__ == "__main__":
    print("📧 Experiment Results Email Checker")
    print("=" * 50)
    
    # Check if email is configured
    if EMAIL_CONFIG['sender_email'] == 'your.email@gmail.com':
        print("\n⚠️  EMAIL NOT CONFIGURED YET!")
        print("\nTo enable email notifications:")
        print("1. Edit email_results.py")
        print("2. Update EMAIL_CONFIG with your email settings")
        print("3. For Gmail: Use an App Password (not your regular password)")
        print("   - Go to: https://myaccount.google.com/apppasswords")
        print("   - Generate an app password for 'Mail'")
        print("\nRunning check anyway (email will fail)...\n")
    
    check_and_notify()
    
    print("\n" + "=" * 50)
    print("✅ Check complete!")
