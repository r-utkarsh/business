param(
    [string]$BrandFile = "selected_brands.csv",
    [string]$ExclusionFile = "brand_exclusions.csv",
    [string]$EnvFile = ".env",
    [string]$OutputDirectory = "logos",
    [int]$Limit = 0
)

function Get-EnvValue([string]$Name) {
    $line = Get-Content $EnvFile | Where-Object { $_ -match "^$Name=" } | Select-Object -First 1
    if (-not $line) { throw "$Name is missing from $EnvFile" }
    $value = $line.Substring($line.IndexOf('=') + 1).Trim().Trim('"')
    if (-not $value) { throw "$Name is empty in $EnvFile" }
    $value
}

function Normalize-Name([string]$Name) {
    $builder = [System.Text.StringBuilder]::new()
    foreach ($character in $Name.Normalize([Text.NormalizationForm]::FormD).ToCharArray()) {
        if ([Globalization.CharUnicodeInfo]::GetUnicodeCategory($character) -ne [Globalization.UnicodeCategory]::NonSpacingMark) {
            [void]$builder.Append($character)
        }
    }
    ($builder.ToString().ToLowerInvariant() -replace '[^a-z0-9]', '')
}

$clientId = Get-EnvValue "BRANDFETCH_CLIENT_ID"
$excluded = @((Import-Csv $ExclusionFile).excluded_name)
$brands = @(Import-Csv $BrandFile | Where-Object { $_.brand -notin $excluded } | Sort-Object brand)
if ($Limit -gt 0) { $brands = @($brands | Select-Object -First $Limit) }

New-Item -ItemType Directory -Force -Path $OutputDirectory | Out-Null
$results = @()
$missing = @()

foreach ($entry in $brands) {
    $name = $entry.brand
    $slug = (($name -replace '[^A-Za-z0-9]+', '-').Trim('-')).ToLowerInvariant()
    $file = Join-Path $OutputDirectory "$slug.svg"

    if (Test-Path $file) {
        $results += [pscustomobject]@{ brand = $name; status = 'existing'; domain = ''; file = $file }
        continue
    }

    try {
        $query = [Uri]::EscapeDataString($name)
        $candidates = @(Invoke-RestMethod -Uri "https://api.brandfetch.io/v2/search/$query?c=$clientId" -TimeoutSec 30)
        $matches = @($candidates | Where-Object { (Normalize-Name $_.name) -eq (Normalize-Name $name) })

        if ($matches.Count -eq 0) {
            $normName = Normalize-Name $name
            $matches = @($candidates | Where-Object { 
                $normCand = Normalize-Name $_.name
                $normCand.Length -ge 3 -and ($normName.StartsWith($normCand) -or $normCand.StartsWith($normName))
            })
        }

        if ($matches.Count -eq 0 -and $candidates.Count -gt 0) {
            $matches = @($candidates | Sort-Object _score -Descending | Select-Object -First 1)
        }

        if ($matches.Count -lt 1) {
            $missing += [pscustomobject]@{ brand = $name; reason = 'No Brandfetch match found'; candidates = ($candidates.name -join ' | ') }
            continue
        }

        $domain = $matches[0].domain
        if (-not $domain) {
            $missing += [pscustomobject]@{ brand = $name; reason = 'Matched brand has no domain'; candidates = $matches[0].name }
            continue
        }

        Invoke-WebRequest -Uri "https://cdn.brandfetch.io/domain/$domain/logo.svg?c=$clientId" -OutFile $file -UseBasicParsing -TimeoutSec 30
        $results += [pscustomobject]@{ brand = $name; status = 'downloaded'; domain = $domain; file = $file }
    }
    catch {
        $missing += [pscustomobject]@{ brand = $name; reason = $_.Exception.Message; candidates = '' }
    }
}

$results | Export-Csv "logo_results.csv" -NoTypeInformation -Encoding utf8
$missing | Export-Csv "missing_logos.csv" -NoTypeInformation -Encoding utf8
Write-Output "Downloaded or reused: $($results.Count)"
Write-Output "Needs review: $($missing.Count)"
