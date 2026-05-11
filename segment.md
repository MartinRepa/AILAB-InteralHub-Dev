Full Project Roadmap - Retail Banking Customer Behavioral Segmentation
1.Project title
Behavioral Segmentation Framework for Retail Banking Customers
2. Project Objective
The objective of this project is to build a customer behavioral segmentation framework for retail banking customers, in order to group customers into meaningful and actionable segments based on how they behave with the bank.
The segmentation should reflect:
•	activity level
•	product usage
•	channel usage
•	transaction behavior
•	relationship development over time
The final result should support:
•	customer profiling
•	campaign targeting
•	digital migration initiatives
•	cross-sell prioritization
•	retention prioritization through overlays
3. Primary use case
Primary use case: Behavioral Segmentation
This means the model should answer:
How do customers behave with the bank?
Not primarily:
•	how profitable they are
•	how risky they are
•	what demographic group they belong to
Those can still be used later as overlay layers.
4. Target population
The target population is:
•	Retail customers
•	Individual customers
•	Active customers
5. Scope of the project
Included in scope
•	customer-level dataset creation
•	variable selection
•	data quality review
•	feature engineering
•	score-based dimension creation
•	clustering with K-Means
•	segment validation
•	segment profiling
•	overlay enrichment
•	implementation-ready output
Out of scope for version 1
•	real-time segmentation
•	full churn prediction model
•	full profitability model
•	next best offer engine
•	production API deployment
•	automated decision engine
6. Core methodological approach
The project should follow this logic:
Raw customer data  variable selection  feature engineering  score-based dimensions  K-Means clustering  overlays  segment  profiling
This structure is the best because:
•	it keeps the model interpretable
•	it keeps the segmentation behavioral
•	it reduces noise from raw variables
•	it makes business adoption easier
7.Recommended project phases
The project should be structured into 4 major phases:
1.	Analysis
2.	Modeling
3.	Validation
4.	Implementation
8. High-level roadmap
Phase 1 – Analysis
Goal: understand the business objective, data sources, and the right variables.
Main outputs:
•	project definition
•	data inventory
•	variable classification
•	input dataset structure
•	feature shortlist
Phase 2 – Modeling
Goal: transform raw data into meaningful model input.
Main outputs:
•	engineered features
•	behavioral dimensions
•	scoring framework
•	clustering input dataset
•	first clustering results
Phase 3 –Validation 
Goal: confirm that the segmentation is statistically sound and business-meaningful.
Main outputs:
•	quality checks
•	clustering evaluation
•	stability checks
•	business validation
•	final segment structure
Phase 4 – Implementation
Goal: make the segmentation usable in practice.
Main outputs:
•	final segment table
•	segment definitions
•	overlays
•	dashboards
•	use-case mapping
•	refresh process

Core Variables
Used directly in clustering
Variable	Status	Dimension	Reason
FrequencyOfCashTransactions6Months	Core	Transaction Style	Measures real intensity of cash usage
NumberOfProductsLast6Month	Core	Product Engagement	Measures active relationship breadth
NumberOfInactiveProducts	Core	Relationship Momentum	Shows products that exist bur are not being used
NewProductsLast6Months	Core	Product Engagement/ Relationship Momentum	Signals exploration and growth of the relationship
ClosedProductsLast6Months	Core	Product Engagement / Relationship Momentum	Signals shrinkage or rationalization of the relationship
HasTibank	Core	Channel Behavior	Distinguishes digital vs non-digital customers
AverageLoginFrequency	Core	Channel Behavior	Measures intensity of platform usage
HasDebitCard	Core	Product Engagement	Indicates basic active product usage
HasCreditCard	Core	Product Engagement	Indicates deeper card-based product usage
CreditCardUsage	Core	Transaction Style	Measures active cars usage
DaysWithoutActivity 	Core	Activity Intensity	Measures how long the customer has been inactive
TimeSinceLastNewProduct	Core	Relationship Momentum	Measures how recently the customer adopted a new product
RecurringTransactions	Core	Activity Intensity	Shows regular and stable usage behavior
TimeSinceLastInteraction	Core	Activity Intensity	Measures how recent the last interaction was
TransactionsLast3Months	Core	Activity Intensity	Captures the most recent customer activity
HasLoanProduct	Core	Product Engagement	Indicates a deeper banking relationship
HasTimeDeposit	Core	Product Engagement	Indicates savings behavior
TibankUsageLast3Months	Core	Channel Behavior	Measures recent digital activity
CustomerUsesTibankPayment	Core	Channel Behavior	Indicates online payment behavior
CustomerUsesTibankOutgoingTransfer	Core 	Channel Behavior	Indicates online transfer behavior
CustomerUsesDeskPayment	Core	Channel Behavior	Indicates reliance on branch/desk
CustomerUsesDeskOutgoingTransfer	Core	Channel Behavior	Indicates branch/desk dependence for transfers
AverageTransactionAmount6M	Core	Transaction Style	Measures average monetary movement size
AverageTransactionSize	Core	Transaction Style	Reflects the style of transactions
NumberOfDirectDebits	Core	Transaction Style	Indicates routine recurring payments
CreditCardUsageVsLimit	Core	Transaction Style	Measures card usage intensity versus limit

Variable Used with Caution
Use selectively or after transformation
Variable	Status	Dimension	Reason
TransactionsLast6Months	Caution	Activity Intensity	Useful as a  stable activity level, but overlaps with recent activity
FrequencyOfCashTransactions3Months	Caution	Activity Intensity	Can be affected by short term seasonality
NumberOfProductsLast3Month	Caution	Product Engagement	More event-driven and overlaps with 6M measure
NewProductsLast3Months	Caution	Product Engagement/ Relationship Momentum	Temporary spike signal
CashWithdrawalFromCreditCard	Caution	Transaction Style	Specified signal not representative
CreditCardUsageAbroad	Caution	Transaction Style	Travel/event-driven behavior, not representative for everyone
WithdrawalsVsDeposits	Caution	Transaction Style	Needs normalization; reflects style rather than level

TibankUsageLast6Months	Caution	Channel Behavior	Better used for trend than as raw core input
PayrollsLast6Months	Caution	Activity Intensity	Similar signal to 3M, often overlapping
PayrollsLast3Months	Caution	Activity Intensity	Shows regularity, bur not full customer behavior
DebitCardUsage6M_vs_3M	Caution	Relationship Momentum	Captures shift from past to recent usage
ATMUsageFrequency6M_vs_3M	Caution	Relationship Momentum	Can signal decline or migration
TibankLastLoginMonths	Caution	Channel Behavior	Good recency signal, but affected by missing-value handling
TibankLastUsedInMonths	Caution	Channel Behavior	Stronger than login recency, but needs clean treatment
AverageProductLifetime	Caution	Product Engagement	Shows loyalty/switching tendency, not necessarily current behavior
AppFeaturesUsed	Caution	Channel Behavior	Good indicator of digital maturity, but must be reliable
IsPayrollCustomer	Caution	Activity Intensity/Overlay	Shows bank anchoring, but not full behavior
NumberOfSavingsAccounts	Caution	Product Engagement	Useful, but may overweight savings behavior
LoanTypeDiversit	Caution	Product Engagement	Shows variety, not always active usage
NumberOfCreditCardTransactionsLastMonth	Caution	Transaction Style	Recent but unstable
NumberOfCreditCardTransactionsLast6Months	Caution	Transaction Style	Useful but overlaps with card usage
NumberOfCreditCardTransactionsLast12Months	Caution	Transaction Style	Ofter redundant
SavingsGrowthRate	Caution	Relationship Momentum	Only meaningful for customers with savings
TransactionsLast12Months	Caution	Activity Intensity	Too broad in time and may dilute recent behavior
ClosedProductsLast3Months	Caution	Relationship Momentum	Short-term signal only
CreditLimitChanges	Caution	Transaction Style	Specific signal, not broadly relevant
HasSalaryIncreaseLast6Months	Caution	Overlay	Event, not base behavior
SeasonalTransactionTrends	Caution	Transaction Style	Needs careful interpretation
SalaryFromCompany	Caution	Overlay	Give context, not behavioral core

Overlay Variables
For interpretation and profiling only
Variable	Status	Dimension	Reason
Age	Overlay	Demographic Overlay	Used for segment interpretation
AgeRange	Overlay	Demographic Overlay	Used for understandable segment naming
Gender	Overlay	Demographic Overlay	Context only
EducationLevel	Overlay	Demographic Overlay	Helps interpret behavior, not define it
MaritalStatus	Overlay	Demographic Overlay	Household context
CustomerLivingRegion	Overlay	Demographic Overlay	Geo context
AvgSalary3Months	Overlay	Value Overlay	Indicates economic level, not behavior
AvgSalary6Months	Overlay	Value Overlay	More stable value-oriented lens
OurFeesComparedToOtherBanks	Overlay	Pricing Overlay	Reflects perception, not behavior
OurInterestVsOtherBanks	Overlay	Pricing Overlay	Reflects opinion/perception, not behavior
HasDefaultHistory	Overlay	Risk/Retention Overlay	Risk ≠ behavior
IncreasedAccountMaintainanceFee	Overlay	Pricing/Retention Overlay	Indicates fee friction
PenaltyFeesPaid	Overlay	Value/Friction Overlay	Indicates cost/friction
CustomerTimeWithBank	Overlay	Value/Stability Overlay	Indicates relationship age
CustomerOrigin	Overlay	Demographic Overlay	Geo context
EmploymentIndustry	Overlay	Demographic Overlay	Context for interpretation
HasChurn History	Overlay	Retention Overlay	Indicates past risk, not base behavior
ChurnFlg	Overlay	Retention Overlay	Target-like variable, not suitable for clustering input
AverageFeePaid	Overlay	Value Overlay	Indicates economic contribution
TimeCurrentJob	Overlay	Demographic/ Stability Overlay	Stability contact


Excluded or Transform-First Variables Not to be used directly in base clustering
Variable	Status	Dimension	Reason
TransactionsLast3/6/12Months together raw	Excluded	Activity Intensity	Redundant; hides trend
FrequencyOfCashTransactions3/6/12Months together raw	Reduce/transform	Activity Intensity	Heavy overlap
NumberOfCreditCardTransactionsLast1/6/12Months	Reduce/transform	Transaction Style	High correlated
PayrollsLast3/6Months	Reduce/transform	Activity Intensity	To much overlap
TibankUsageLast3/6Months together raw	Reduce/transform	Channel Behavior	Better as base + trend
NumberOfProductsLast3/6Month  together raw	Reduce/transform	Product Engagement/	Very similar signal
NewProductsLast3/6Months	Reduce/transform	Product Engagement/ Relationship Momentum	Same signal across different windows
ClosedProductsLast3/6Months	Reduce/transform	Product Engagement/ Relationship Momentum	Same signal across different windows
ID	None	None	Only an identifier

1.	What can we do with Caution variables?
These variables are not bad. They are useful, but they should not go directly and strongly into the base clustering model.
We can se them in 4 main ways:
A.	Use them after transformation
Instead of using them raw, convert them into:
•	Trends
•	Ratios
•	Flags
•	Grouped bands
Examples:
•	TransactionsLast6Months  using it to create ActivityTrend
•	TibankUsageLast6Months  using it to create DigitalTrend
•	PayrollsLast6Months  using it to create PayrollStability
•	SavingsGrowthRate  using it as part of RelationshipMomentum

B.	Use them with lower weight in scoring
If they are helpful but not strong enough, include them in a dimension with smaller influence.
Examples:
•	AppFeaturesUsed can support Channel Bahvior
•	NumberOfSavingsAccounts  can support Product Engagement
•	WithdrawalsVsDeposits  can support Transaction Style

C.	Use them for challenger models
We can build:
•	One base model with only core variables
•	One challenger version with some caution variables added
Then compare:
•	Cluster quality
•	Interpretability
•	Stability

D.	Use them for profiling after clustering
Even if they do not enter base model, they can still help describe the segment.

2.	What we can do with Overlay variables?
Overlay variables are very important, but not for building the base behavioral clusters.
We use them after clustering.
They help in 3 main ways:
A.	Segment Interpretation
Once the cluster are build. Overlays tell you:
•	wich segment has higher retention risk
•	wich segment has higher value
•	wich segment is younger, older, urban, etc.
Example:
•	Segment = Digital Active Customers
•	Retention Overlay = Low Risk
•	Value Overlay = High Value
•	Demographic Overlay = Age 25-40, Urban

B.	Prioritization
Two segments may have similar behavior, but one may be valuable.
Example: 
•	Segment A = behavioral segment
•	High Value overlay = priority for premium offers
•	Medium Value overlay = second priority 

C.	Actioning
Overlays help decide what action to take.
Examples:
•	Behavioral segment + higher retention risk  retention action
•	Behavioral segment + high value  premium relationship action
•	Behavioral segment + certain demographic profile  targeted campaign
So overlays are for:
•	Profiling
•	Prioritization
•	Business action
Not for defining the behavioral core.
3.	What can we do with Excluded variables?
Excluded variables are not necessarily useless. They are just not suitable in their current form.
We can use them in 3 ways
A.	Transform them
Examples: 
TransactionsLast3/6/12Months together raw  turn them into: 
•	recent activity
•	long-term activity
•	activity trend
TibankUsageLast3/6Months together raw  turn into:
•	current digital level
•	digital trend

B.	Clean them first
If variables has:
•	-999
•	Too many nulls
•	Unclear meaning

C.	Keep them out permanently if they add no value
