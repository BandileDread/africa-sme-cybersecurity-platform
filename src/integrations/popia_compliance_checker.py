#!/usr/bin/env python3
"""
POPIA Compliance Checker - AfriSec Integration Module
Copyright (c) 2026 BandileDread (AfriSec Platform)

This module represents YOUR IP - the integration logic that checks
system configurations against POPIA (Protection of Personal Information Act)
requirements for South African SMEs.

It uses open-source tools/config parsers underneath but applies
custom business logic specific to POPIA compliance.
"""

import os
import json
import yaml
import logging
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from pathlib import Path

logger = logging.getLogger(__name__)

@dataclass
class POPIARequirement:
    """Represents a specific POPIA requirement"""
    section: str
    requirement_id: str
    description: str
    check_type: str  # 'config', 'process', 'technical'
    severity: str    # 'high', 'medium', 'low'
    remediation: str

@dataclass
class ComplianceResult:
    """Result of a POPIA compliance check"""
    requirement: POPIARequirement
    status: str      # 'compliant', 'non_compliant', 'not_applicable', 'error'
    evidence: str
    details: Optional[str] = None
    remediation_advice: Optional[str] = None

class POPIAChecker:
    """
    Main POPIA compliance checking engine
    
    This is YOUR IP: The specific logic that maps technical/system checks
    to POPIA requirements for South African context.
    """
    
    def __init__(self, config_path: str = "./configs/"):
        self.config_path = Path(config_path)
        self.requirements = self._load_popia_requirements()
        self.findings: List[ComplianceResult] = []
        
    def _load_popia_requirements(self) -> List[POPIARequirement]:
        """Load POPIA requirements - could be from DB, config, or hardcoded for MVP"""
        # In a real implementation, this might load from a database or external source
        # For now, we define key POPIA sections that map to technical controls
        return [
            POPIARequirement(
                section="Chapter 8 - Conditions for lawful processing",
                requirement_id="POPIA_8_1",
                description="Personal information must be processed lawfully and in a reasonable manner",
                check_type="process",
                severity="high",
                remediation="Implement data processing consent management and purpose limitation controls"
            ),
            POPIARequirement(
                section="Chapter 9 - Further processing limitation",
                requirement_id="POPIA_9_1", 
                description="Personal information must not be further processed incompatibly",
                check_type="process",
                severity="high", 
                remediation="Implement data classification and purpose binding controls"
            ),
            POPIARequirement(
                section="Chapter 10 - Information quality",
                requirement_id="POPIA_10_1",
                description="Responsible party must ensure completeness and accuracy of personal information", 
                check_type="process",
                severity="medium",
                remediation="Implement data validation and quality assurance processes"
            ),
            POPIARequirement(
                section="Chapter 12 - Security safeguards",
                requirement_id="POPIA_12_1_a",
                description="Appropriate technical measures to protect integrity of personal information",
                check_type="technical",
                severity="high",
                remediation="Implement encryption at rest and in transit, access controls, and integrity checks"
            ),
            POPIARequirement(
                section="Chapter 12 - Security safeguards", 
                requirement_id="POPIA_12_1_b",
                description="Appropriate organisational measures to protect integrity of personal information",
                check_type="process",
                severity="high",
                remediation="Implement security policies, training, and access management procedures"
            ),
            POPIARequirement(
                section="Chapter 12 - Security safeguards",
                requirement_id="POPIA_12_2", 
                description="If processing involves a unique identifier, implement additional safeguards",
                check_type="technical", 
                severity="medium",
                remediation="Implement pseudonymization or additional encryption for unique identifiers"
            ),
            POPIARequirement(
                section="Chapter 13 - Security safeguards",
                requirement_id="POPIA_13_1",
                description="Notify regulator and data subjects of breaches where reasonable",
                check_type="process",
                severity="high", 
                remediation="Implement breach detection, assessment, and notification procedures"
            ),
            POPIARequirement(
                section="Chapter 14 - Further processing",
                requirement_id="POPIA_14_1",
                description="Prior written authorization required for special personal information processing",
                check_type="config",
                severity="high",
                remediation="Implement approval workflows and special data handling procedures"
            )
        ]
        
    def check_config_file(self, filepath: str) -> List[ComplianceResult]:
        """
        Check a configuration file for POPIA-relevant settings
        
        This is where YOUR IP shines: Applying POPIA-specific logic to 
        generic configuration data from open-source tools.
        """
        results = []
        path = Path(filepath)
        
        if not path.exists():
            logger.warning(f"Config file not found: {filepath}")
            return results
            
        try:
            # Handle different file types
            if path.suffix in ['.yaml', '.yml']:
                with open(path) as f:
                    config = yaml.safe_load(f)
            elif path.suffix == '.json':
                with open(path) as f:
                    config = json.load(f)
            else:
                # Treat as plain text/ini
                with open(path) as f:
                    config = {'raw_content': f.read()}
                    
            # Apply POPIA-specific checks to the configuration
            results.extend(self._check_encryption_settings(config, path))
            results.extend(self._check_access_controls(config, path))
            results.extend(self._check_data_retention(config, path))
            results.extend(self._check_audit_logging(config, path))
            
        except Exception as e:
            logger.error(f"Error checking config file {filepath}: {e}")
            results.append(ComplianceResult(
                requirement=POPIARequirement(
                    section="General", 
                    requirement_id="CONFIG_ERROR",
                    description=f"Failed to parse configuration file: {filepath}",
                    check_type="technical",
                    severity="high",
                    remediation="Fix configuration file syntax"
                ),
                status="error",
                evidence=str(e),
                details="Configuration file could not be parsed"
            ))
            
        return results
        
    def _check_encryption_settings(self, config: Dict, filepath: Path) -> List[ComplianceResult]:
        """Check for encryption-related POPIA requirements"""
        results = []
        
        # POPIA 12.1_a: Technical measures for integrity
        encryption_found = False
        encryption_details = []
        
        # Check various places encryption might be configured
        encryption_paths = [
            ['security', 'encryption', 'enabled'],
            ['database', 'ssl', 'enabled'], 
            ['network', 'tls', 'enabled'],
            ['encryption', 'at_rest'],
            ['encryption', 'in_transit'],
            ['ssl', 'enabled'],
            ['tls', 'enabled']
        ]
        
        for path in encryption_paths:
            if self._get_nested_value(config, path):
                encryption_found = True
                encryption_details.append(f"Found encryption at {'.'.join(path)}")
                
        if encryption_found:
            results.append(ComplianceResult(
                requirement=POPIARequirement(
                    section="Chapter 12 - Security safeguards",
                    requirement_id="POPIA_12_1_a",
                    description="Appropriate technical measures to protect integrity of personal information",
                    check_type="technical",
                    severity="high",
                    remediation="Encryption appears to be configured - verify key management and strength"
                ),
                status="compliant",
                evidence="; ".join(encryption_details),
                details=f"Encryption settings found in {filepath.name}"
            ))
        else:
            results.append(ComplianceResult(
                requirement=POPIARequirement(
                    section="Chapter 12 - Security safeguards",
                    requirement_id="POPIA_12_1_a", 
                    description="Appropriate technical measures to protect integrity of personal information",
                    check_type="technical",
                    severity="high",
                    remediation="Configure encryption for data at rest and in transit (TLS, AES-256, etc.)"
                ),
                status="non_compliant",
                evidence="No encryption settings detected in configuration",
                details=f"Check {filepath.name} for encryption, TLS, or SSL settings"
            ))
            
        return results
        
    def _check_access_controls(self, config: Dict, filepath: Path) -> List[ComplianceResult]:
        """Check access control configurations"""
        results = []
        
        # POPIA related to access controls and authorization
        auth_enabled = self._get_nested_value(config, ['security', 'authentication', 'enabled']) or \
                      self._get_nested_value(config, ['auth', 'enabled']) or \
                      self._get_nested_value(config, ['access_control', 'enabled'])
                      
        if auth_enabled:
            results.append(ComplianceResult(
                requirement=POPIARequirement(
                    section="Chapter 12 - Security safeguards",
                    requirement_id="POPIA_12_1_b",
                    description="Appropriate organisational measures to protect integrity of personal information", 
                    check_type="process",
                    severity="high",
                    remediation="Authentication enabled - verify MFA and least privilege implementation"
                ),
                status="compliant",
                evidence="Authentication system enabled",
                details=f"Access controls found in {filepath.name}"
            ))
        else:
            results.append(ComplianceResult(
                requirement=POPIARequirement(
                    section="Chapter 12 - Security safeguards",
                    requirement_id="POPIA_12_1_b",
                    description="Appropriate organisational measures to protect integrity of personal information",
                    check_type="process", 
                    severity="high",
                    remediation="Implement authentication and authorization mechanisms (MFA, RBAC, etc.)"
                ),
                status="non_compliant",
                evidence="No authentication/access control settings detected",
                details=f"Check {filepath.name} for auth, access_control, or security settings"
            ))
            
        return results
        
    def _check_data_retention(self, config: Dict, filepath: Path) -> List[ComplianceResult]:
        """Check data retention and minimization (POPIA principles)"""
        results = []
        
        # Check for data retention policies
        retention_days = self._get_nested_value(config, ['data', 'retention', 'days']) or \
                        self._get_nested_value(config, ['privacy', 'retention_days']) or \
                        self._get_nested_value(config, ['records', 'retention_days'])
                        
        if retention_days is not None:
            if isinstance(retention_days, (int, float)) and retention_days <= 365:  # Reasonable retention
                results.append(ComplianceResult(
                    requirement=POPIARequirement(
                        section="Chapter 11 - Further processing limitation",
                        requirement_id="POPIA_11_2",
                        description="Personal information not retained longer than necessary",
                        check_type="process",
                        severity="medium", 
                        remediation="Retention period configured - verify it aligns with business needs and legal requirements"
                    ),
                    status="compliant",
                    evidence=f"Data retention set to {retention_days} days",
                    details=f"Retention policy found in {filepath.name}"
                ))
            else:
                results.append(ComplianceResult(
                    requirement=POPIARequirement(
                        section="Chapter 11 - Further processing limitation",
                        requirement_id="POPIA_11_2",
                        description="Personal information not retained longer than necessary", 
                        check_type="process",
                        severity="medium",
                        remediation="Review and set appropriate data retention period (typically <= 365 days for most SME data)"
                    ),
                    status="non_compliant",
                    evidence=f"Data retention set to {retention_days} days (may be excessive)",
                    details=f"Consider data minimization principles in {filepath.name}"
                ))
        # If no retention setting found, it's not necessarily non-compliant - might be handled elsewhere
        else:
            results.append(ComplianceResult(
                requirement=POPIARequirement(
                    section="Chapter 11 - Further processing limitation",
                    requirement_id="POPIA_11_2",
                    description="Personal information not retained longer than necessary",
                    check_type="process",
                    severity="low",  # Lower severity as this might be handled procedurally
                    remediation="Consider implementing explicit data retention policies"
                ),
                status="not_applicable",
                evidence="No explicit data retention setting found",
                details=f"Data retention may be managed procedurally or in other systems"
            ))
            
        return results
        
    def _check_audit_logging(self, config: Dict, filepath: Path) -> List[ComplianceResult]:
        """Check audit logging and monitoring (POPIA accountability)"""
        results = []
        
        # POPIA requires ability to demonstrate compliance (audit trails)
        audit_enabled = self._get_nested_value(config, ['logging', 'audit', 'enabled']) or \
                       self._get_nested_value(config, ['audit', 'enabled']) or \
                       self._get_nested_value(config, ['security', 'monitoring', 'enabled'])
                       
        if audit_enabled:
            results.append(ComplianceResult(
                requirement=POPIARequirement(
                    section="Chapter 12 - Security safeguards", 
                    requirement_id="POPIA_12_1_c",  # Hypothetical extension for audit
                    description="Audit trails to demonstrate compliance with POPIA requirements",
                    check_type="technical",
                    severity="medium",
                    remediation="Audit logging enabled - verify logs are protected and reviewed regularly"
                ),
                status="compliant",
                evidence="Audit logging or security monitoring enabled",
                details=f"Monitoring/audit found in {filepath.name}"
            ))
        else:
            results.append(ComplianceResult(
                requirement=POPIARequirement(
                    section="Chapter 12 - Security safeguards",
                    requirement_id="POPIA_12_1_c",
                    description="Audit trails to demonstrate compliance with POPIA requirements", 
                    check_type="technical",
                    severity="medium",
                    remediation="Enable audit logging and security monitoring to track access to personal information"
                ),
                status="non_compliant",
                evidence="No audit logging or security monitoring detected",
                details=f"Enable logging, auditing, or monitoring features in {filepath.name}"
            ))
            
        return results
        
    def _get_nested_value(self, data: Dict, path: List[str]) -> any:
        """Safely get nested value from dictionary"""
        current = data
        for key in path:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return None
        return current
        
    def run_full_assessment(self, config_paths: List[str] = None) -> Dict:
        """
        Run a full POPIA compliance assessment
        
        Returns a structured report suitable for management or auditors
        """
        if config_paths is None:
            # Default config locations to check
            config_paths = [
                "./configs/",
                "./docker-compose.yml", 
                "./.env",
                "./nginx/",
                "./apache2/"
            ]
            
        # Filter to existing paths
        existing_paths = [p for p in config_paths if os.path.exists(p)]
        
        all_results = []
        for path in existing_paths:
            if os.path.isfile(path):
                results = self.check_config_file(path)
                all_results.extend(results)
            elif os.path.isdir(path):
                for root, dirs, files in os.walk(path):
                    for file in files:
                        if file.endswith(('.yaml', '.yml', '.json', '.conf', '.config', '.ini', '.txt', '.env')):
                            filepath = os.path.join(root, file)
                            results = self.check_config_file(filepath)
                            all_results.extend(results)
                            
        # Generate summary report
        compliant = len([r for r in all_results if r.status == 'compliant'])
        non_compliant = len([r for r in all_results if r.status == 'non_compliant'])
        errors = len([r for r in all_results if r.status == 'error'])
        not_applicable = len([r for r in all_results if r.status == 'not_applicable'])
        
        summary = {
            'timestamp': str(Path.cwd()),
            'total_checks': len(all_results),
            'compliant': compliant,
            'non_compliant': non_compliant,
            'errors': errors,
            'not_applicable': not_applicable,
            'compliance_percentage': round((compliant / max(len(all_results), 1)) * 100, 2),
            'findings': [
                {
                    'requirement_id': r.requirement.requirement_id,
                    'section': r.requirement.section,
                    'description': r.requirement.description,
                    'status': r.status,
                    'evidence': r.evidence,
                    'remediation': r.requirement.remediation,
                    'severity': r.requirement.severity
                }
                for r in all_results
            ]
        }
        
        self.findings = all_results
        return summary
        
    def generate_report(self, format: str = 'json') -> str:
        """Generate a compliance report in various formats"""
        report = self.run_full_assessment()
        
        if format == 'json':
            return json.dumps(report, indent=2)
        elif format == 'markdown':
            return self._generate_markdown_report(report)
        else:
            return str(report)
            
    def _generate_markdown_report(self, report: Dict) -> str:
        """Generate a human-readable markdown compliance report"""
        md = f"""# POPIA Compliance Assessment Report

**Generated**: {report['timestamp']}  
**Overall Compliance**: {report['compliance_percentage']}% ({report['compliant']}/{report['total_checks']} checks passed)

## Summary
- ✅ **Compliant**: {report['compliant']}
- ❌ **Non-Compliant**: {report['non_compliant']}  
- ⚠️ **Errors**: {report['errors']}
- ℹ️ **Not Applicable**: {report['not_applicable']}

## Detailed Findings

| Requirement ID | Section | Description | Status | Severity | Evidence |
|----------------|---------|-------------|--------|----------|----------|
"""
        
        for finding in report['findings']:
            status_emoji = {
                'compliant': '✅',
                'non_compliant': '❌', 
                'error': '⚠️',
                'not_applicable': 'ℹ️'
            }.get(finding['status'], '❓')
            
            md += f"| {finding['requirement_id']} | {finding['section'][:30]}... | {finding['description'][:40]}... | {status_emoji} {finding['status']} | {finding['severity']} | {finding['evidence'][:30]}... |\n"
            
        md += "\n## Recommendations\n\n"
        non_compliant_findings = [f for f in report['findings'] if f['status'] == 'non_compliant']
        if non_compliant_findings:
            md += "### High Priority Items\n"
            high_priority = [f for f in non_compliant_findings if f['severity'] == 'high']
            for finding in high_priority[:5]:  # Top 5
                md += f"- **{finding['requirement_id']}**: {finding['requirement']} - {finding['remediation']}\n"
                
            medium_priority = [f for f in non_compliant_findings if f['severity'] == 'medium']
            for finding in medium_priority[:3]:  # Top 3
                md += f"- **{finding['requirement_id']}**: {finding['requirement']} - {finding['remediation']}\n"
        else:
            md += "Excellent! No non-compliant findings detected. Regular assessments recommended.\n"
            
        return md

def main():
    """CLI entry point for the POPIA compliance checker"""
    import argparse
    
    parser = argparse.ArgumentParser(description='AfriSec POPIA Compliance Checker')
    parser.add_argument('--config', '-c', help='Path to config file or directory to check')
    parser.add_argument('--format', '-f', choices=['json', 'markdown', 'text'], default='json',
                       help='Output format for the report')
    parser.add_argument('--output', '-o', help='Output file path (default: stdout)')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose logging')
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.WARNING)
        
    checker = POPIAChecker()
    
    if args.config:
        if os.path.isfile(args.config):
            results = checker.check_config_file(args.config)
            print(f"Checked {len(results)} requirements in {args.config}")
            for r in results:
                print(f"  {r.requirement.requirement_id}: {r.status}")
        elif os.path.isdir(args.config):
            # Check all config files in directory
            config_files = []
            for root, dirs, files in os.walk(args.config):
                for file in files:
                    if file.endswith(('.yaml', '.yml', '.json', '.conf', '.config', '.ini', '.txt', '.env')):
                        config_files.append(os.path.join(root, file))
                        
            all_results = []
            for config_file in config_files:
                results = checker.check_config_file(config_file)
                all_results.extend(results)
                print(f"Checked {len(results)} requirements in {config_file}")
                
            # Generate summary
            report = checker.run_full_assessment(config_files)
            output = checker.generate_report(args.format)
        else:
            print(f"Error: Path not found: {args.config}")
            return 1
    else:
        # Run full assessment on default locations
        report = checker.run_full_assessment()
        output = checker.generate_report(args.format)
        
    if args.output:
        with open(args.output, 'w') as f:
            f.write(output)
        print(f"Report written to {args.output}")
    else:
        print(output)
        
    return 0

if __name__ == "__main__":
    exit(main())